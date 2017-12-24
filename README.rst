================
payeer_api
================

payeer_api - Реализация клиента для Payeer API.

До использования следует ознакомиться с официальной документацией
Payeer (https://payeercom.docs.apiary.io/). Приложение реализует
протокол взаимодействия, описанный в этом документе.

Установка
=========

::

    $ pip install payeer_api

Использование
=============

Пример::

from payeer_api import PayeerAPI

account = 'P1000000'
api_id = '123456789'
api_pass = 'KRicaFodFrgJer6'

p = PayeerAPI(account, api_id, api_pass)

p.get_balance()