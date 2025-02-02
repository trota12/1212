document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".login-form");

    form.addEventListener("submit", function (event) {
        let isValid = true;

        const username = document.querySelector("[name='username']");
        const email = document.querySelector("[name='email']");
        const password = document.querySelector("[name='password']");

        // Reset estilos
        [username, email, password].forEach(input => {
            input.classList.remove("error");
        });

        // Validar nombre de usuario
        if (username.value.trim() === "") {
            showError(username, "El nombre de usuario es obligatorio.");
            isValid = false;
        }

        // Validar email con expresión regular
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email.value)) {
            showError(email, "Ingrese un email válido.");
            isValid = false;
        }

        // Validar contraseña (mínimo 6 caracteres)
        if (password.value.length < 6) {
            showError(password, "La contraseña debe tener al menos 6 caracteres.");
            isValid = false;
        }

        // Si hay errores, detener el envío del formulario
        if (!isValid) {
            event.preventDefault();
        }
    });

    // Función para mostrar errores
    function showError(input, message) {
        input.classList.add("error");
        const errorText = document.createElement("div");
        errorText.className = "error-text";
        errorText.textContent = message;
        input.parentNode.appendChild(errorText);
    }
});
