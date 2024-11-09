# -*- coding: utf-8 -*-

import re
from odoo import models, fields, api
from odoo.api import ValuesType
from odoo.exceptions import ValidationError

ESTADOS = [
    ("alta", "Alta"),
    ("baja", "Baja"),
    ("borrador", "Borrador"),
]
class Paciente(models.Model):
    _name = "vertical_hospital.paciente"
    _description = "Paciente de un hospital"

    _inherit = ["mail.thread", "mail.activity.mixin"]

    secuencia = fields.Char(
        string="Secuencia",
        required=True,
        readonly=True,
        copy=False,
        default="Nuevo",
    )
    nombre_completo = fields.Char(string="Nombre y apellido", required=True)
    rnc = fields.Char(
        string="RNC", required=True, size=15, help="000-0000000-0", tracking=True
    )
    tratamiento_id = fields.Many2many(
        "vertical_hospital.tratamiento",
        string="Tratamientos",
        required=True,
    )
    fecha_de_alta = fields.Datetime(string="Fecha de alta")
    fecha_de_actualizacion = fields.Datetime(string="Fecha de actualizacion")
    estado = fields.Selection(
        selection=ESTADOS, string="Estado", default=ESTADOS[0][0], tracking=True
    )

    @api.model_create_single
    def create(self, vals):
        if vals.get("secuencia", "Nuevo") == "Nuevo":
            vals["secuencia"] = (
                self.env["ir.sequence"].next_by_code("paciente.pa") or "Nuevo"
            )
        if vals.get("estado") not in dict(self._fields["estado"].selection):
            raise ValueError("Invalid value for estado: %s" % vals.get("estado"))
        return super(Paciente, self).create(vals)

    def write(self, vals):
        if "estado" in vals and vals["estado"] not in dict(
            self._fields["estado"].selection
        ):
            raise ValueError("Invalid value for estado: %s" % vals["estado"])
        return super(Paciente, self).write(vals)

    @api.model_create_multi
    def create_multi(self, vals):
        for val in vals:
            if val.get("secuencia", "Nuevo") == "Nuevo":
                val["secuencia"] = (
                    self.env["ir.sequence"].next_by_code("paciente.pa") or "Nuevo"
                )
            if val.get("estado") not in dict(self._fields["estado"].selection):
                raise ValueError("Invalid value for estado: %s" % val.get("estado"))
        return super(Paciente, self).write(vals)

    @api.onchange()
    def write(self, vals):
        vals["fecha_de_actualizacion"] = fields.Datetime.now()
        return super(Paciente, self).write(vals)

    @api.constrains("rnc")
    def check_rnc_format(self):
        """Validación para que el RNC solo acepte el formato correcto"""
        print("check_rnc_format", self.rnc)
        for record in self:
            # Eliminar cualquier caracter no numérico
            rnc_clean = re.sub(r"\D", "", record.rnc)
            if len(rnc_clean) != 11:
                raise ValidationError("El RNC debe tener 11 caracteres numéricos.")
            if not re.match(r"^\d{3}\d{7}\d{1}$", rnc_clean):
                raise ValidationError(
                    "El RNC debe tener el formato correcto: 00000000000"
                )

        self.rnc = re.sub(r"(\d{3})(\d{7})(\d{1})", r"\1-\2-\3", rnc_clean)

class Tratamiento(models.Model):
    # _codigo = "vertical_hospital.tratamiento.codigo"
    _name = "vertical_hospital.tratamiento"
    # _medico_tratante = "vertical_hospital.tratamiento.medico_tratante"
    _description = "Tratamiento de un paciente"

    codigo = fields.Char(
        string="Código del Tratamiento",
        required=True,
        readonly=True,
        copy=False,
        default="Codigo",
    )
    name = fields.Char(string="Nombre del Tratamiento", required=True)
    medico_tratante = fields.Char(string="Médico tratante")
    descripcion = fields.Text(string="Descripción")
    # secuencia_paciente = fields.Many2many(
    #     "vertical_hospital.paciente", string="Secuencia del paciente"
    # )

    @api.model_create_single
    def create(self, vals) -> ValuesType:
        if vals.get("codigo", "Codigo") == "Codigo":
            vals["codigo"] = (
                self.env["ir.sequence"].next_by_code("tratamiento.codigo") or "Codigo"
            )
        return super(Tratamiento, self).create(vals)

    @api.model_create_multi
    def create_multi(self, vals):
        for val in vals:
            if val.get("codigo", "Codigo") == "Codigo":
                val["secuencia"] = (
                    self.env["ir.sequence"].next_by_code("tratamiento.codigo")
                    or "Codigo"
                )

        return super(Tratamiento, self).create(vals)