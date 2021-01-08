#!/usr/bin/env python3
# -*- coding:utf-8 -*-


class Variable(object):
    """全局变量池"""

    def set(self, key, value):
        setattr(self, key, value)

    def get(self, key):
        return getattr(self, key)

    def has(self, key):
        return hasattr(self, key)


is_vars = Variable()

if __name__ == '__main__':
    is_vars.set('name', 'hoou')
    print(is_vars.get('name'))
