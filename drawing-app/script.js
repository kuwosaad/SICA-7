const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

let tool = 'pencil';
let drawing = false;
let startX = 0;
let startY = 0;
let color = document.getElementById('colorPicker').value;
let brushSize = document.getElementById('brushSize').value;

const undoStack = [];
const redoStack = [];

function pushState() {
    undoStack.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
    if (undoStack.length > 50) undoStack.shift();
    redoStack.length = 0;
}

function restoreState(stackFrom, stackTo) {
    if (stackFrom.length === 0) return;
    stackTo.push(ctx.getImageData(0, 0, canvas.width, canvas.height));
    const state = stackFrom.pop();
    ctx.putImageData(state, 0, 0);
}

document.querySelectorAll('[data-tool]').forEach(btn => {
    btn.addEventListener('click', () => {
        tool = btn.getAttribute('data-tool');
    });
});

document.getElementById('colorPicker').addEventListener('change', e => {
    color = e.target.value;
});

document.getElementById('brushSize').addEventListener('change', e => {
    brushSize = e.target.value;
});

canvas.addEventListener('mousedown', e => {
    drawing = true;
    startX = e.offsetX;
    startY = e.offsetY;
    ctx.lineCap = 'round';
    ctx.strokeStyle = color;
    ctx.lineWidth = brushSize;
    if (tool === 'pencil' || tool === 'eraser') {
        pushState();
        ctx.beginPath();
        ctx.moveTo(startX, startY);
        if (tool === 'eraser') ctx.globalCompositeOperation = 'destination-out';
        else ctx.globalCompositeOperation = 'source-over';
    }
});

canvas.addEventListener('mousemove', e => {
    if (!drawing) return;
    const x = e.offsetX;
    const y = e.offsetY;

    if (tool === 'pencil' || tool === 'eraser') {
        ctx.lineTo(x, y);
        ctx.stroke();
    }
});

canvas.addEventListener('mouseup', e => {
    if (!drawing) return;
    drawing = false;
    const x = e.offsetX;
    const y = e.offsetY;
    if (tool === 'pencil' || tool === 'eraser') {
        ctx.closePath();
        ctx.globalCompositeOperation = 'source-over';
    } else {
        pushState();
        drawShape(tool, startX, startY, x, y);
    }
});

function drawShape(type, x0, y0, x1, y1) {
    ctx.strokeStyle = color;
    ctx.lineWidth = brushSize;
    switch (type) {
        case 'line':
            ctx.beginPath();
            ctx.moveTo(x0, y0);
            ctx.lineTo(x1, y1);
            ctx.stroke();
            ctx.closePath();
            break;
        case 'rect':
            ctx.strokeRect(Math.min(x0,x1), Math.min(y0,y1), Math.abs(x1-x0), Math.abs(y1-y0));
            break;
        case 'circle':
            const radius = Math.hypot(x1 - x0, y1 - y0);
            ctx.beginPath();
            ctx.arc(x0, y0, radius, 0, Math.PI * 2);
            ctx.stroke();
            ctx.closePath();
            break;
    }
}

document.getElementById('undoBtn').addEventListener('click', () => restoreState(undoStack, redoStack));
document.getElementById('redoBtn').addEventListener('click', () => restoreState(redoStack, undoStack));

document.getElementById('saveBtn').addEventListener('click', () => {
    const link = document.createElement('a');
    link.href = canvas.toDataURL('image/png');
    link.download = 'drawing.png';
    link.click();
});

document.getElementById('imageLoader').addEventListener('change', e => {
    const file = e.target.files[0];
    if (!file) return;
    const img = new Image();
    const reader = new FileReader();
    reader.onload = evt => {
        img.onload = () => {
            pushState();
            ctx.drawImage(img, 0, 0);
        };
        img.src = evt.target.result;
    };
    reader.readAsDataURL(file);
});

canvas.addEventListener('click', e => {
    if (tool !== 'text' || drawing) return;
    const text = prompt('Enter text:');
    if (text) {
        pushState();
        ctx.fillStyle = color;
        ctx.font = `${brushSize * 4}px sans-serif`;
        ctx.fillText(text, e.offsetX, e.offsetY);
    }
});
