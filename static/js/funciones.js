// Funciones relacionadas con el RUT

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

// Función para formatear el RUT
function formatRutInput(event) {
    const input = event.target;
    let value = input.value.replace(/\./g, '').replace(/-/g, ''); // Elimina puntos y guiones

    if (value.length >= 1) {
        // Inserta el guion antes del último dígito
        const rutBody = value.slice(0, -1); // Parte del RUT sin el último dígito
        const dv = value.slice(-1); // Último dígito (dígito verificador)

        // Formatear con puntos cada 3 dígitos
        const formattedRut = rutBody.replace(/\B(?=(\d{3})+(?!\d))/g, '.') + '-' + dv;
        input.value = formattedRut; // Asigna el valor formateado al input
    } else {
        input.value = ''; // Si no hay valor, limpiar el campo
    }
}

// Funciones relacionadas con la renta

// Función para formatear el número en miles
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

// Función para manejar el input de renta
function formatRentaInput(event) {
    const input = event.target;
    let value = input.value.replace(/\./g, ''); // Elimina puntos existentes
    if (!isNaN(value) && value !== '') {
        input.value = formatNumber(value); // Formatea el número
    } else {
        input.value = ''; // Si no es un número válido, lo limpia
    }
}

// Funciones relacionadas con regiones y comunas

// Función para filtrar comunas según la región seleccionada
function filterComunas(regionSelect, comunaSelect) {
    const regionId = regionSelect.value;
    const options = comunaSelect.options;
    for (let i = 0; i < options.length; i++) {
        const option = options[i];
        const region = option.getAttribute('data-region');

        if (region == regionId) {
            option.style.display = 'block';
        } else {
            option.style.display = 'none';
        }
    }
}

// Función para limitar la fecha de nacimiento a hace más de 10 años
function limitFechaNacimiento() {
    const fechaInputs = document.querySelectorAll('#fecha_nacimiento');
    fechaInputs.forEach(fechaInput => {
        if (!fechaInput) return;  // Verificar que el campo existe

        const hoy = new Date();
        
        // Calcular la fecha límite de hace 10 años
        const fechaLimite = new Date();
        fechaLimite.setFullYear(hoy.getFullYear() - 10);
        
        // Formatear la fecha como YYYY-MM-DD
        const dia = String(fechaLimite.getDate()).padStart(2, '0');
        const mes = String(fechaLimite.getMonth() + 1).padStart(2, '0'); // Los meses en JavaScript son base 0
        const anio = fechaLimite.getFullYear();
        
        // Asignar la fecha máxima permitida
        fechaInput.setAttribute('max', `${anio}-${mes}-${dia}`);
        
        // Validación: mostrar un mensaje si la fecha es mayor que la permitida
        fechaInput.addEventListener('change', function () {
            const fechaSeleccionada = new Date(fechaInput.value);
            if (fechaSeleccionada > fechaLimite) {
                alert('La fecha seleccionada debe ser de más de 10 años.');
                fechaInput.value = ''; // Limpiar el campo si la fecha es inválida
            }
        });
    });
}

// Código que se ejecuta al cargar el documento
document.addEventListener('DOMContentLoaded', function () {
    // Aplicar formateo de RUT a todos los campos con clase 'rut-input'
    const rutInputs = document.querySelectorAll('.rut-input');
    rutInputs.forEach(function (rutInput) {
        rutInput.addEventListener('input', formatRutInput);
    });

    // Validar RUT en todos los formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(function (form) {
        form.addEventListener('submit', function (event) {
            const rutInputs = form.querySelectorAll('.rut-input');
            rutInputs.forEach(function (rutInput) {
                const rutValue = rutInput.value.trim();
                if (!validarRut(rutValue)) {
                    alert('El RUT ingresado en el formulario no es válido');
                    event.preventDefault(); // Evitar envío del formulario si el RUT no es válido
                }
            });
        });
    });

    // Aplicar formateo de renta a todos los campos con clase 'renta-input'
    const rentaInputs = document.querySelectorAll('.renta-input');
    rentaInputs.forEach(function (rentaInput) {
        rentaInput.value = formatNumber(rentaInput.value.replace(/\./g, '')); // Formatear el valor inicial
        rentaInput.addEventListener('input', formatRentaInput);
    });

    // Aplicar filtrado de comunas a todos los pares de selectores de región y comuna
    const regionSelects = document.querySelectorAll('.region-select');
    regionSelects.forEach(function (regionSelect) {
        const comunaSelect = document.querySelector(`.comuna-select[data-region-select="${regionSelect.id}"]`);
        if (comunaSelect) {
            filterComunas(regionSelect, comunaSelect); // Filtrar comunas al cargar la página
            regionSelect.addEventListener('change', function () {
                filterComunas(regionSelect, comunaSelect);
                comunaSelect.value = ''; // Limpiar selección de comuna
            });
        }
    });

    // Establecer la fecha mínima de nacimiento
    limitFechaNacimiento();
});