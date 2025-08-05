"""
Application configuration settings
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Security settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Database settings
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///webapp.db'
    
    # API settings
    API_RATE_LIMIT = "100 per hour"
    API_VERSION = "v1"
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = 'webapp.log'

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False
    
    # Override with more secure settings
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

class TestingConfig(Config):
    """Testing environment configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'

# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(environment='default'):
    """
    Get configuration for specified environment
    
    Args:
        environment (str): Environment name
        
    Returns:
        Config: Configuration class instance
    """
    return config_map.get(environment, DevelopmentConfig)
