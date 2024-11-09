// odoo.define('vertical_hospital.validate_rnc', function (require) {
//     "use strict";

//     var FormController = require('web.FormController');
//     var core = require('web.core');
//     var _t = core._t;

//     FormController.include({
//         // Sobrescribimos el método de inicialización
//         start: function () {
//             this._super.apply(this, arguments);
//             // Escuchar el evento de entrada en el campo RNC
//             this._onInputRNC();
//         },

//         // Método para escuchar cambios en el campo RNC
//         _onInputRNC: function () {
//             var self = this;
//             // Asegúrate de que 'rnc' es el nombre correcto del campo
//             this.$el.on('input', 'input[name="rnc"]', function (event) {
//                 self._validateRNC(event);
//             });
//         },

//         // Método para validar el RNC
//         _validateRNC: function (event) {
//             var campoNameValue = this.model.get('rnc'); // Obtener el valor del campo RNC
//             if (!campoNameValue) {
//                 this.displayNotification({
//                     type: 'danger',
//                     title: _t('Validación fallida'),
//                     message: _t('El campo "rnc" no puede estar vacío.')
//                 });
//                 return;  // Salir si está vacío
//             }

//             // Eliminar caracteres no numéricos
//             campoNameValue = campoNameValue.replace(/\D/g, '');

//             // Validación del formato del RNC
//             var regex = /^\d{3}-\d{7}-\d{1}$/;
//             if (!regex.test(campoNameValue)) {
//                 this.displayNotification({
//                     type: 'danger',
//                     title: _t('Validación fallida'),
//                     message: _t('El formato del campo "rnc" debe ser XXX-XXXXXXX-X.')
//                 });
//                 return;  // Salir si no coincide con el formato
//             }

//             // Formatear y actualizar el RNC
//             campoNameValue = campoNameValue.replace(/(\d{3})(\d{7})(\d{1})/, '$1-$2-$3');
//             this.model.set({ 'rnc': campoNameValue });  // Actualiza el modelo con el valor formateado
//         },
//     });
// });

// const rncValidate = (input) => {
//     var rnc = input.value;
//     rnc = rnc.replace(/\D/g, '');

//     var rncRegex = /^\d{3}-\d{7}-\d{1}$/;
        
//     if (!rncRegex.test(rnc)) {
//         input.style.borderColor = "red";
//         input.setCustomValidity('El rnc no es valido')
//         input.value = ''
//     }else{
//         input.style.borderColor = "green";
//         input.setCustomValidity('')
//         input.value = rnc.replace(/(\d{3})(\d{7})(\d{1})/, '$1-$2-$3');
//     }       
// }

    // core.action_registry.add('vertical_hospital.paciente', {
    //     start: function () {
    //         var input = document.querySelector('[name="rnc"]');
    //         if (!input) return;
    //         input.addEventListener('input', function () {
    //             rncValidate(input);
    //         })
    //     }
    // });