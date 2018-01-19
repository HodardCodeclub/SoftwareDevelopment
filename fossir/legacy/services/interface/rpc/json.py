# This file is part of fossir.
# Copyright (C) 2002 - 2017 European Organization for Nuclear Research (CERN).
#
# fossir is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# fossir is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fossir; if not, see <http://www.gnu.org/licenses/>.

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
