let joystickData = {
    esquerdo: { tipo: 'esquerdo', forca: 0, angulo: 0 },
    direito: { tipo: 'direito', forca: 0, angulo: 0 }
};

function sendJoystickData() {
    fetch('/control', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(joystickData)
    }).catch(error => {
        console.error('Erro ao enviar os dados do joystick:', error);
    });
}