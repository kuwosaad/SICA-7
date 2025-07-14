const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let drawing = false;
let currentTool = 'pencil';
let startX, startY;
let undoStack = [];
let redoStack = [];

function saveState() {
    undoStack.push(canvas.toDataURL());
    redoStack = [];
}

function restoreState(stack, opposite) {
    if (stack.length) {
        opposite.push(canvas.toDataURL());
        const img = new Image();
        img.src = stack.pop();
        img.onload = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0);
        };
    }
}

canvas.addEventListener('mousedown', (e) => {
    drawing = true;
    ctx.strokeStyle = document.getElementById('colorPicker').value;
    ctx.lineWidth = document.getElementById('sizePicker').value;
    ctx.lineCap = 'round';
    startX = e.offsetX;
    startY = e.offsetY;
    if (currentTool === 'pencil' || currentTool === 'eraser') {
        ctx.beginPath();
        ctx.moveTo(startX, startY);
    }
});

canvas.addEventListener('mousemove', (e) => {
    if (!drawing) return;
    const x = e.offsetX;
    const y = e.offsetY;
    if (currentTool === 'pencil') {
        ctx.lineTo(x, y);
        ctx.stroke();
    } else if (currentTool === 'eraser') {
        ctx.strokeStyle = '#ffffff';
        ctx.lineTo(x, y);
        ctx.stroke();
    }
});

canvas.addEventListener('mouseup', (e) => {
    if (!drawing) return;
    drawing = false;
    const x = e.offsetX;
    const y = e.offsetY;
    if (currentTool === 'rect') {
        ctx.strokeRect(startX, startY, x - startX, y - startY);
    } else if (currentTool === 'circle') {
        const radius = Math.hypot(x - startX, y - startY);
        ctx.beginPath();
        ctx.arc(startX, startY, radius, 0, Math.PI * 2);
        ctx.stroke();
    } else if (currentTool === 'line') {
        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.lineTo(x, y);
        ctx.stroke();
    } else if (currentTool === 'text') {
        const text = prompt('Enter text');
        if (text) ctx.fillText(text, x, y);
    }
    saveState();
});

canvas.addEventListener('mouseleave', () => {
    drawing = false;
});

// Tool buttons
for (const btn of document.querySelectorAll('#toolbar button[data-tool]')) {
    btn.addEventListener('click', () => {
        document.querySelector('#toolbar button.active').classList.remove('active');
        btn.classList.add('active');
        currentTool = btn.dataset.tool;
    });
}

// Undo/Redo
document.getElementById('undo').addEventListener('click', () => restoreState(undoStack, redoStack));
document.getElementById('redo').addEventListener('click', () => restoreState(redoStack, undoStack));

document.getElementById('save').addEventListener('click', () => {
    const link = document.createElement('a');
    link.download = 'drawing.png';
    link.href = canvas.toDataURL();
    link.click();
});

document.getElementById('imageLoader').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (evt) => {
        const img = new Image();
        img.onload = () => {
            ctx.drawImage(img, 0, 0);
            saveState();
        };
        img.src = evt.target.result;
    };
    reader.readAsDataURL(file);
});

saveState();
