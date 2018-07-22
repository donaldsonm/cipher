document.addEventListener('DOMContentLoaded', function() {

    if (window.location.pathname == '/affine') {

        document.querySelector('#encrypt_affine').addEventListener("click", function(event) {
            event.preventDefault();

            const request = new XMLHttpRequest();
            const text = document.querySelector('#text').value;
            const a = document.querySelector('#a').value;
            const b = document.querySelector('#b').value;

            request.open('POST', '/affine/encrypt');

            request.onload = function() {

                const data = JSON.parse(request.responseText);

                if (data.success == "success") {
                    document.querySelector('#result').innerHTML = data.ciphertext;
                }
                if (data.success == "error1") {
                    document.querySelector('#result').innerHTML = 'error: missing text';
                }
                if (data.success == "error2") {
                    document.querySelector('#result').innerHTML = "error: missing 'a' value";
                }
                if (data.success == "error3") {
                    document.querySelector('#result').innerHTML = "error: missing 'b' value";
                }
                if (data.success == "error4") {
                    document.querySelector('#result').innerHTML = "error: invalid 'a' value";
                }

            };

            const data = new FormData();
            data.append('text', text);
            data.append('a', a);
            data.append('b', b);

            request.send(data);
            return false;
        });

        document.querySelector('#decrypt_affine').addEventListener("click", function(event) {
            event.preventDefault();

            const request = new XMLHttpRequest();
            const text = document.querySelector('#text').value;
            const a = document.querySelector('#a').value;
            const b = document.querySelector('#b').value;

            request.open('POST', '/affine/decrypt');

            request.onload = function() {

                const data = JSON.parse(request.responseText);

                if (data.success == "success") {
                    document.querySelector('#result').innerHTML = data.plaintext;
                }
                if (data.success == "error1") {
                    document.querySelector('#result').innerHTML = 'error: missing text';
                }
                if (data.success == "error2") {
                    document.querySelector('#result').innerHTML = "error: missing 'a' value";
                }
                if (data.success == "error3") {
                    document.querySelector('#result').innerHTML = "error: missing 'b' value";
                }
                if (data.success == "error4") {
                    document.querySelector('#result').innerHTML = "error: invalid 'a' value";
                }

            };

            const data = new FormData();
            data.append('text', text);
            data.append('a', a);
            data.append('b', b);

            request.send(data);
            return false;
        });

    }


    if (window.location.pathname == '/caesar') {

        document.querySelector('#encrypt_caesar').addEventListener("click", function(event) {
            event.preventDefault();

            const request = new XMLHttpRequest();
            const text = document.querySelector('#text').value;
            const shift = document.querySelector('#shift').value;

            request.open('POST', '/caesar/encrypt');

            request.onload = function() {

                const data = JSON.parse(request.responseText);

                if (data.success == "success") {
                    document.querySelector('#result').innerHTML = data.ciphertext;
                }
                if (data.success == "error1") {
                    document.querySelector('#result').innerHTML = 'error: missing text';
                }
                if (data.success == "error2") {
                    document.querySelector('#result').innerHTML = 'error: missing shift value';
                }

            };

            const data = new FormData();
            data.append('text', text);
            data.append('shift', shift);

            request.send(data);
            return false;
        });


        document.querySelector('#decrypt_caesar').addEventListener("click", function(event) {
            event.preventDefault();

            const request = new XMLHttpRequest();
            const text = document.querySelector('#text').value;
            const shift = document.querySelector('#shift').value;

            request.open('POST', '/caesar/decrypt');

            request.onload = function() {

                const data = JSON.parse(request.responseText);

                if (data.success == "success") {
                    document.querySelector('#result').innerHTML = data.plaintext;
                }
                if (data.success == "error1") {
                    document.querySelector('#result').innerHTML = 'error: missing text';
                }
                if (data.success == "error2") {
                    document.querySelector('#result').innerHTML = 'error: missing shift value';
                }

            };

            const data = new FormData();
            data.append('text', text);
            data.append('shift', shift);

            request.send(data);
            return false;
        });
    }


    if (window.location.pathname == '/vigenere') {

        document.querySelector('#encrypt_vigenere').addEventListener("click", function(event) {
            event.preventDefault();

            const request = new XMLHttpRequest();
            const text = document.querySelector('#text').value;
            const key = document.querySelector('#key').value;

            request.open('POST', '/vigenere/encrypt');

            request.onload = function() {

                const data = JSON.parse(request.responseText);

                if (data.success == "success") {
                    document.querySelector('#result').innerHTML = data.ciphertext;
                }
                if (data.success == "error1") {
                    document.querySelector('#result').innerHTML = 'error: missing text';
                }
                if (data.success == "error2") {
                    document.querySelector('#result').innerHTML = 'error: missing key';
                }
                if (data.success == "error3") {
                    document.querySelector('#result').innerHTML = 'error: key can only contain alphabetic characters';
                }

            };

            const data = new FormData();
            data.append('text', text);
            data.append('key', key);

            request.send(data);
            return false;
        });

        document.querySelector('#decrypt_vigenere').addEventListener("click", function(event) {
            event.preventDefault();

            const request = new XMLHttpRequest();
            const text = document.querySelector('#text').value;
            const key = document.querySelector('#key').value;

            request.open('POST', '/vigenere/decrypt');

            request.onload = function() {

                const data = JSON.parse(request.responseText);

                if (data.success == "success") {
                    document.querySelector('#result').innerHTML = data.plaintext;
                }
                if (data.success == "error1") {
                    document.querySelector('#result').innerHTML = 'error: missing text';
                }
                if (data.success == "error2") {
                    document.querySelector('#result').innerHTML = 'error: missing key';
                }
                if (data.success == "error3") {
                    document.querySelector('#result').innerHTML = 'error: key can only contain alphabetic characters';
                }

            };

            const data = new FormData();
            data.append('text', text);
            data.append('key', key);

            request.send(data);
            return false;

        });

    }

})