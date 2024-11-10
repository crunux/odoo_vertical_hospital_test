# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request


class VerticalHospital(http.Controller):
    @http.route(
        "/vertical_hospital/",
        type="http",
        auth="public",
    )
    def index(self, **kw):
        return "Hola, mundo"

# endpoint web server by params secuencia
class Pacientes(http.Controller):
    @http.route(
        "/pacientes/consulta/<secuencia>",
        type="http",
        auth="public",
        methods=["GET"],
    )
    def paciente(self, secuencia, **kw):
        paciente = (
            request.env["vertical_hospital.paciente"]
            .search([("secuencia", "=", secuencia)])
            .read()
        )
        output = {
            "sec": paciente[0]["secuencia"],
            "name": paciente[0]["nombre_completo"],
            "rnc": paciente[0]["rnc"],
            "state": paciente[0]["estado"],
        }
        return json.dumps(output)
