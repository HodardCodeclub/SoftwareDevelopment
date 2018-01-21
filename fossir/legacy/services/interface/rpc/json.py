

from flask import jsonify, request

from fossir.core.logger import Logger
from fossir.legacy.common.fossilize import clearCache
from fossir.legacy.services.interface.rpc.process import invoke_method


def process():
    clearCache()
    payload = request.json
    Logger.get('rpc').info('json rpc request. request: %r', payload)
    rv = {}
    if 'id' in payload:
        rv['id'] = payload['id']
    rv['result'] = invoke_method(str(payload['method']), payload.get('params', []))
    return jsonify(rv)
