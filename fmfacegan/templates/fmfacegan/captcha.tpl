<script src="https://www.google.com/recaptcha/api.js?render={{ recapcha_key }}"></script>
<script>
    grecaptcha.ready(function() {
        grecaptcha.execute('{{ recapcha_key }}', {action:'validate_captcha'})
            .then(function(token) {
                document.getElementById('g_recaptcha_response').value = token;
            });
    });
</script>