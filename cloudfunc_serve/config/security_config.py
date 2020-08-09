# coding=utf-8

from guniflask.context import configuration
from guniflask.security_config import WebSecurityConfigurer, HttpSecurity, enable_web_security


@configuration
@enable_web_security
class SecurityConfiguration(WebSecurityConfigurer):

    def configure_http(self, http: HttpSecurity):
        """Configure http security here"""
