var username = document.querySelector('.username')
var email = document.querySelector('.email')
var password = document.querySelector('.password')
var repassword = document.querySelector('.repassword')
var form = document.querySelector('form')

function showError(input, message)
{
    let parent = input.parentElement;
    let small = parent.querySelector('small')
    parent.classList.add('error')
    small.innerText = message
}

function showSucces(input)
{
    let parent = input.parentElement;
    let small = parent.querySelector('small')
    parent.classList.remove('error')
    small.innerText = ''
}

function checkEmptyError(listInput)
{
    let isEmptyError = false;
    listInput.forEach( input => 
    {
        input.value = input.value.trim()

        if(!input.value)
        {
            isEmptyError = true
            showError( input, 'Không được để trống')
        }
        else
        {
            showSucces(input)
        }
    });
    return isEmptyError
}

function checkEmailError(input)
{
    const regexEmail = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    input.value = input.value.trim()
    let isEmailError = !regexEmail.test(input.value)
    if( regexEmail.test(input.value))
    {
        showSucces()
    }
    else
    {
        showError(input, 'Email không hợp lệ')
    }
    return isEmailError;
}

function checkLengthError( input, max, min)
{
    input.value = input.value.trim()
    if( input.value.length < min)
    {
        showError(input, `Phải có ít nhất ${min} kí tự`)
        return true
    }
    if(input.value.length > max)
    {
        showError(input, `Không được quá ${max} kí tự`)
        return true
    }
    showSucces(input)
    return false;
}

function checkMatchPass(passInput, passConfirm)
{
    if( passInput.value !== passConfirm.value)
    {
        showError(passConfirm, 'PassWord không trùng khớp')
        return true
    }
    return false;
}

form.addEventListener('submit', function(event)
{
    let isEmptyError = checkEmptyError([username, email, password, repassword]);
    let isEmailError = checkEmailError(email);  
    let isUserNameLengthError = checkLengthError( username, 10, 5);
    let isPassWordLengthError = checkLengthError(password, 10, 5);
    let isMatchError = checkMatchPass(password, repassword);

    if (isEmptyError || isEmailError || isUserNameLengthError || isPassWordLengthError || isMatchError) {
        event.preventDefault(); // Ngăn chặn form từ việc gửi nếu có lỗi
    }
})



