function calculateJoystickSize() {
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;
    return Math.min(screenWidth * 0.2, screenHeight * 0.15);
}

const getCommonOptions = () => ({
    mode: 'static',
    color: '#4285F4',
    size: calculateJoystickSize(),
    threshold: 0.1,
    fadeTime: 250,
    maxNumberOfNipples: 1,
    dataOnly: false,
    lockY: false,
    lockX: false,
    maxPressure: 1,
    restOpacity: 0.7
});

let joystickLeft, joystickRight;

function createJoysticks() {
    if (joystickLeft) joystickLeft.destroy();
    if (joystickRight) joystickRight.destroy();

    joystickLeft = nipplejs.create({
        ...getCommonOptions(),
        zone: document.getElementById('joystickLeft'),
        position: { left: '70%', top: '70%' }
    });

    joystickRight = nipplejs.create({
        ...getCommonOptions(),
        zone: document.getElementById('joystickRight'),
        position: { left: '30%', top: '70%' },
        color: '#EA4335'
    });

    setupJoystickEvents(joystickLeft, 'Left');
    setupJoystickEvents(joystickRight, 'Right');
}

function setupJoystickEvents(manager, side) {
    const outputEl = document.querySelector(`#output${side} p:first-child`);
    const directionEl = document.getElementById(`direction${side}`);
    const forceEl = document.getElementById(`force${side}`);
    const angleEl = document.getElementById(`angle${side}`);

    manager.on('start move', function(evt, nipple) {
        const angle = Math.round(nipple.angle?.degree || 0);
        const force = Math.min(1, Math.round(nipple.force * 100) / 100);

        outputEl.textContent = `Joystick ${side === 'Left' ? 'Direito' : 'Esquerdo'} ativado`;
        outputEl.style.color = side === 'Left' ? '#4285F4' : '#EA4335';
        directionEl.textContent = `Direção: ${getDirectionName(angle)}`;
        forceEl.textContent = `Força: ${force}`;
        angleEl.textContent = `Ângulo: ${angle}°`;

        if (side === 'Left') {
            joystickData.esquerdo = { tipo: 'esquerdo', forca: force, angulo: angle };
        } else {
            joystickData.direito = { tipo: 'direito', forca: force, angulo: angle };
        }

        sendJoystickData();
    });

    manager.on('end', function() {
        outputEl.textContent = `Joystick ${side === 'Left' ? 'Esquerdo' : 'Direito'} liberado`;
        outputEl.style.color = '#666';
        directionEl.textContent = 'Direção: -';
        forceEl.textContent = 'Força: 0';
        angleEl.textContent = 'Ângulo: 0°';

        if (side === 'Left') {
            joystickData.esquerdo = { tipo: 'esquerdo', forca: 0, angulo: 0 };
        } else {
            joystickData.direito = { tipo: 'direito', forca: 0, angulo: 0 };
        }

        sendJoystickData();
    });
}


function getDirectionName(angle) {
    if (angle === undefined) return '-';

    const directions = [
        'Direita', 'Frente-Direita', 'Frente', 'Frente-Esquerda',
        'Esquerda', 'Trás-Esquerda', 'Trás', 'Trás-Direita',
    ];

    const index = Math.round(((angle % 360) / 45)) % 8;
    return directions[index];
}

createJoysticks();

window.addEventListener('resize', () => {
    createJoysticks();
});
