


// #FUNCION PARA SELECCIONAR LA REGIÓN Y QUE MUESTRE SOLO LAS COMUNAS DE LA REGIÓN

document.addEventListener('DOMContentLoaded', function() {
    // Manejador de eventos para el cambio en el selector de regiones
    document.getElementById('region').addEventListener('change', function() {
        var regionId = this.value;
        var comunas = document.querySelectorAll('#comuna option');
        
        // Iterar sobre todas las opciones de comuna
        comunas.forEach(function(comuna) {
            var comunaRegionId = comuna.getAttribute('data-region');
            
            // Mostrar u ocultar la opción de comuna según la región seleccionada
            if (comunaRegionId == regionId || comunaRegionId == '') {
                comuna.style.display = 'block';
            } else {
                comuna.style.display = 'none';
            }
        });
    });
});




// #---------------------------------------------------------------------------------------------

//FUNCIONES DE VALIDACIÓN PARA EL RUT

document.addEventListener('DOMContentLoaded', function() {
    // Función para validar un RUT chileno
    function validarRut(rut) {
        rut = rut.replace(/\./g, ''); // Eliminar puntos
        rut = rut.replace('-', ''); // Eliminar guión

        var rutSinDV = rut.slice(0, -1); // Obtener solo el número del RUT
        var dv = rut.slice(-1).toUpperCase(); // Obtener el dígito verificador

        // Validar que el RUT tenga formato numérico válido
        if (!/^[0-9]+$/.test(rutSinDV) || (rutSinDV.length < 7)) {
            return false;
        }

        // Calcular dígito verificador esperado
        var suma = 0;
        var multiplo = 2;

        for (var i = rutSinDV.length - 1; i >= 0; i--) {
            suma += parseInt(rutSinDV.charAt(i)) * multiplo;
            if (multiplo < 7) {
                multiplo += 1;
            } else {
                multiplo = 2;
            }
        }

        var dvEsperado = 11 - (suma % 11);

        // Tratar casos especiales para dígito verificador
        dvEsperado = (dvEsperado === 11) ? 0 : ((dvEsperado === 10) ? 'K' : dvEsperado.toString());

        // Comparar dígito verificador ingresado con dígito verificador esperado
        return (dv == dvEsperado);
    }

    // Agregar evento de escucha al formulario de perfil para validar el RUT
    var formPerfil = document.getElementById('profile_form');
    if (formPerfil) {
        formPerfil.addEventListener('submit', function(event) {
            var rutInput = document.getElementById('profile.rut');
            var rutValue = rutInput.value.trim();
            if (!validarRut(rutValue)) {
                alert('El RUT ingresado no es válido');
                event.preventDefault(); // Evitar envío del formulario si el RUT no es válido
            }
        });
    }
});