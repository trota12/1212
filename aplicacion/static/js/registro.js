document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".registro-form");

    form.addEventListener("submit", function (event) {
        const rut = document.querySelector("input[name='rut']");
        const email = document.querySelector("input[name='email']");
        const password1 = document.querySelector("input[name='password1']");
        const password2 = document.querySelector("input[name='password2']");

        let isValid = true;

        // Validar RUT
        if (!validarRUT(rut.value)) {
            alert("El RUT ingresado no es válido.");
            isValid = false;
        }

        // Validar contraseña
        if (password1.value !== password2.value) {
            alert("Las contraseñas no coinciden.");
            isValid = false;
        }

        if (!isValid) {
            event.preventDefault();
        }
    });

    function validarRUT(rut) {
        // Implementa validación de RUT chileno aquí
        return /^[0-9]+-[0-9Kk]$/.test(rut);
    }
});
