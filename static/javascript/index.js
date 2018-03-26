const last_channel = localStorage.getItem('last_channel')
const user_name = localStorage.getItem('user_name')
const current_url = window.location.href;

if (last_channel === null || user_name === null) {
    new_url = current_url + 'login';
    console.log('NEW:' + new_url);
    window.location.replace(new_url);

}
else {
    new_url = current_url + 'chat/' + last_channel;
    console.log('NEW:' + new_url);
    window.location.replace(new_url);
}