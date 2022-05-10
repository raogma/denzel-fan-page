export async function sendRequest(url, method, body, csrf_token){
    let options = {
        method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
        },
    };

    if (body){
        options['body'] = JSON.stringify(body);
    }
    let res = await fetch(url, options);
    if (res.status === 204){
        return;
    }
    return res.json();
}