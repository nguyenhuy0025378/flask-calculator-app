import os
from app import create_app
from app.config import DevelopmentConfig, ProductionConfig

config_mapping = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

config_name = os.environ.get('FLASK_ENV', 'development')
config_class = config_mapping.get(config_name, DevelopmentConfig)

app = create_app(config_class)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=config_class.DEBUG)