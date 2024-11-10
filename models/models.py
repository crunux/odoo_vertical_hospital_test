# -*- coding: utf-8 -*-

import re
from odoo import _, models, fields, api
from odoo.api import ValuesType
from odoo.exceptions import ValidationError

# state of a paciente
ESTADOS = [
    ("alta", "Alta"),
    ("baja", "Baja"),
    ("borrador", "Borrador"),
]

# Model of Paciente
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
        string="RNC", required=True, size=15, help="00000000000", tracking=True
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

    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id, string='Company')

    # Méthod to report print
    def action_print_report(self):
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            return
        pacientes = self.browse(active_ids)
        return self.env.ref('vertical_hospital.report_paciente_list_hospital').report_action(pacientes)

    # # method to when create a new record to auto generate a code and validate state
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

    # method to when create a multi record to auto generate a code and validate state
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

    # method to when update a record
    @api.onchange()
    def write(self, vals):
        vals["fecha_de_actualizacion"] = fields.Datetime.now()
        return super(Paciente, self).write(vals)

    # method to validate the RNC
    @api.constrains("rnc")
    def check_rnc_format(self):
        """Validación para que el RNC solo acepte el formato correcto"""
        print("check_rnc_format", self.rnc)
        rnc_clean = ""
        for record in self:
            # Eliminar cualquier caracter no numérico
            rnc_clean = re.sub(r"\D", "", record.rnc)
            if len(rnc_clean) != 11:
                raise ValidationError("El RNC debe tener 11 caracteres numéricos.")
            if not re.match(r"^\d{3}\d{7}\d{1}$", rnc_clean):
                raise ValidationError(
                    "El RNC debe tener el formato correcto: 00000000000"
                )


# Model of Tratamiento
class Tratamiento(models.Model):
    _name = "vertical_hospital.tratamiento"
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

    # method to when create a new record to auto generate a code and validate state
    @api.model_create_single
    def create(self, vals) -> ValuesType:
        if vals.get("codigo", "Codigo") == "Codigo":
            vals["codigo"] = (
                self.env["ir.sequence"].next_by_code("tratamiento.codigo") or "Codigo"
            )
        return super(Tratamiento, self).create(vals)

    # method to when create a multi record to auto generate a code and validate state
    @api.model_create_multi
    def create_multi(self, vals):
        for val in vals:
            if val.get("codigo", "Codigo") == "Codigo":
                val["secuencia"] = (
                    self.env["ir.sequence"].next_by_code("tratamiento.codigo")
                    or "Codigo"
                )

        return super(Tratamiento, self).create(vals)

class ReportPaciente(models.AbstractModel):
    _name = 'report.vertical_hospital.report_paciente_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        pacientes = self.env['vertical_hospital.paciente'].browse(docids)
        return {
            'doc_ids': docids,
            'docs': pacientes,
        }

# Model of Configuracion
class Configuracion(models.TransientModel):
    _name = "vertical_hospital.settings"
    _description = "Configuración de Vertical Hospital"
    _inherit = "res.config.settings"

    webservice_endpoint = fields.Char("Webservice Endpoint", readonly=False, config_parameter='vertical_hospital.webservice.endpoint')

    # method to save the configuration
    def set_values(self):
        res = super(Configuracion, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('vertical_hospital.webservice.endpoint', self.webservice_endpoint)
        return res

    # method to get the configuration
    def get_values(self):
        res = super(Configuracion, self).get_values()
        webservice_endpoint = self.env['ir.config_parameter'].sudo().get_param('vertical_hospital.webservice.endpoint')
        res.update(webservice_endpoint=webservice_endpoint)
        return res