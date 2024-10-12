<script>
    let startTime = localStorage.getItem('gradientStartTime');

    if (!startTime) {
        startTime = Date.now();
        localStorage.setItem('gradientStartTime', startTime);
    }

    const elapsedTime = (Date.now() - startTime) / 1000;

    const body = document.getElementById('animatedBody');
    body.style.animationDelay = `-${elapsedTime % 15}s`;  
</script>
