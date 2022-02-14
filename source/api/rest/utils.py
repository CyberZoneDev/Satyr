import json


class Reply:
    @staticmethod
    def ok(**kwargs) -> tuple:
        if not kwargs:
            return json.dumps({'status': True, 'response': {'message': 'OK'}}), 200
        return json.dumps({'status': True, 'response': kwargs}), 200

    @staticmethod
    def bad_request(**kwargs) -> tuple:
        if not kwargs:
            return json.dumps({'status': False, 'response': {'error': 'Bad request'}}), 400
        return json.dumps({'status': False, 'response': kwargs}), 400

    @staticmethod
    def forbidden(**kwargs) -> tuple:
        if not kwargs:
            return json.dumps({'status': False, 'response': {'error': 'Forbidden'}}), 403
        return json.dumps({'status': False, 'response': kwargs}), 403

    @staticmethod
    def not_found(**kwargs) -> tuple:
        if not kwargs:
            return json.dumps({'status': False, 'response': {'error': 'Not found'}}), 404
        return json.dumps({'status': False, 'response': kwargs}), 404

    @staticmethod
    def conflict(**kwargs) -> tuple:
        if not kwargs:
            return json.dumps({'status': False, 'response': {'error': 'Conflict'}}), 409
        return json.dumps({'status': False, 'response': kwargs}), 409

    @staticmethod
    def unknown_error(**kwargs) -> tuple:
        if not kwargs:
            return json.dumps({'status': False, 'response': {'error': 'Something went wrong...'}}), 520
        return json.dumps({'status': False, 'response': kwargs}), 520

    @staticmethod
    def failed_dependency(**kwargs) -> tuple:
        if not kwargs:
            return json.dumps({'status': False, 'response': {'error': 'Failed dependency'}}), 424
        return json.dumps({'status': False, 'response': kwargs}), 424