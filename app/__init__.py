from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_stats_controller import api as user_ns
from .main.controller.chat_stats_controller import api as chat_ns
#from .main.controller.master_stats_controller import api as master_ns


blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='TRUECHAT STATISTICS',
          version='1.0',
          description='Statistics microservice for TrueChat app'
          )

api.add_namespace(user_ns, path='/api/user')
api.add_namespace(chat_ns, path='/api/chat')
#api.add_namespace(diagnosis_ns, path='/api/master')
