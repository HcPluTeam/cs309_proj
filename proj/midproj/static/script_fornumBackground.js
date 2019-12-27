(function () {

    var unit = 100,
        canvas,ctx,
        height, width, xAxis, yAxis,
        draw;

    function init() {
        canvas = document.getElementById("canvas");
        canvas.width = document.documentElement.clientWidth;
        canvas.height = document.documentElement.clientHeight;
        ctx = canvas.getContext("2d");
        width = canvas.width;
        height = canvas.height;
        xAxis = Math.floor(height / 2);
        yAxis = 0;
        draw();
    }

    function draw() {
        ctx.clearRect(0, 0, width, height);
        drawWave(0.3, 6, 8000);
        draw.seconds = draw.seconds + .014;
        draw.t = draw.seconds * Math.PI;
        setTimeout(draw, 35);
    };
    draw.seconds = 0;
    draw.t = 0;

    function drawWave(alpha, zoom, delay) {
        var color = ctx.createLinearGradient(0, 0, width, height);
        color.addColorStop(0, '#72c7fe');
        color.addColorStop(1, '#a2e2ff');
        ctx.fillStyle = color;
        ctx.globalAlpha = alpha;
        ctx.beginPath();
        drawSine(draw.t / 0.5, zoom, delay);
        ctx.lineTo(width + 10, height);
        ctx.lineTo(0, height);
        ctx.closePath();
        ctx.fill();
    }

    function drawSine(t, zoom, delay) {

        var x = t;
        var y = Math.sin(x) / zoom;
        ctx.moveTo(yAxis, unit * y + xAxis);
        for (i = yAxis; i <= width + 10; i += 10) {
            x = t + (-yAxis + i) / unit / zoom;
            y = Math.sin(x - delay) / 10;
            ctx.lineTo(i, unit * y + xAxis);
        }
    }

    init();

})();