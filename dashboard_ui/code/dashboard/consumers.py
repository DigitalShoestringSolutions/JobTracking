from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
import requests
import zmq
import asyncio

from zmq.asyncio import Context

context = Context.instance()

zmq_config = {
    "wrapper_out": {
        "type": zmq.PUSH,
        "address": "tcp://127.0.0.1:6000",
        "bind": True,
    },
    "state_in": {
        "type": zmq.PULL,
        "address": "tcp://127.0.0.1:6000",
        "bind": False,
    },
    "state_out": {
        "type": zmq.PUSH,
        "address": "tcp://127.0.0.1:6001",
        "bind": False,
    },
    "wrapper_in": {
        "type": zmq.PULL,
        "address": "tcp://127.0.0.1:6001",
        "bind": True,
    },
}

wrapper_group_name = "wrapper_in"


class StateUpdateConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        zmq_in_conf = zmq_config["state_in"]
        self.zmq_in = context.socket(zmq_in_conf["type"])
        if zmq_in_conf["bind"]:
            self.zmq_in.bind(zmq_in_conf["address"])
        else:
            self.zmq_in.connect(zmq_in_conf["address"])

        zmq_out_conf = zmq_config["state_out"]
        self.zmq_out = context.socket(zmq_out_conf["type"])
        if zmq_out_conf["bind"]:
            self.zmq_out.bind(zmq_out_conf["address"])
        else:
            self.zmq_out.connect(zmq_out_conf["address"])

        loop = asyncio.get_running_loop()
        loop.create_task(self.handle_incomming())

        await self.accept()

    async def disconnect(self, close_code):
        print("disconnect")
        pass

    async def receive_json(self, content):
        print(f"Websocket got:{content}")
        tag = content.get("tag", None)
        content = content.get("content", None)
        if tag is not None and content is not None:
            print("sending on channel layer")
            await self.zmq_out.send_json(
                {
                    "topic": f"feeds/{tag}",
                    "payload": content,
                }
            )

    async def handle_incomming(self):
        while True:
            msg = await self.zmq_in.recv()
            msg_json = json.loads(msg)
            await self.mqtt_update(msg_json)

    async def mqtt_update(self, message):
        print("CONSUMER GOT", message)
        payload = message["payload"]
        if payload["state"] == "entered" or payload["state"] == "changed":
            ws_message = payload
            await self.send_json(
                {
                    "tag": "state-update",
                    "content": ws_message,
                },
            )
