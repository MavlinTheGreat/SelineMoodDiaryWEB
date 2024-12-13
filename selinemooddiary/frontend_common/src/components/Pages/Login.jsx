import React, { useState } from 'react';
import '../../static/css/login.css'

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    {/*const [data, setData] = useState(null);*/}
    
    const [data, setData] = useState(
        {
            loginsuccess: true,
        }
    );

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        {/*try {
            const response = await fetch('https://api.example.com/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username: email, password }),
            });

            if (response.ok) {
                const data = await response.json();
                // Сохраняем токен или другую необходимую информацию
                localStorage.setItem('token', data.token);
                alert('Вы успешно вошли!');
                // Здесь можно перенаправить пользователя на другую страницу
            } else {
                const errorData = await response.json();
                setError(errorData.message || 'Ошибка авторизации');
            }
        } catch (err) {
            setError('Произошла ошибка при подключении к серверу');
        } finally {
            setLoading(false);
        }*/}
        
        data.loginsuccess ? alert('Вы успешно вошли!') : alert('Вы успешно не вошли!');

        setLoading(false);
    };

    return (
        <div className='login-page'>
            <h2>Войти</h2>
            <form onSubmit={handleSubmit}>
                <div className='form-field'>
                    <label htmlFor='email-input'>Электронная почта:<br></br>
                        <input
                            type="text"
                            id='email-input'
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            style={{
                                minWidth: "15em",
                                width: `${email.length * 0.75}em`,
                                maxWidth: "30em"
                            }}
                            required
                        />
                    </label>
                </div><br></br>
                <div className='form-field'>
                    <label>Пароль:<br></br>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            style={{
                                minWidth: "10em",
                                width: `${password.length * 0.75}em`,
                                maxWidth: "20em"
                            }}
                            required
                        />
                    </label>
                </div><br></br>
                <button type="submit" disabled={loading}>
                    {loading ? 'Загрузка...' : 'Войти'}
                </button>
                {error && <p style={{ color: 'red' }}>{error}</p>}
            </form>
            
            <input type="checkbox" checked={data.loginsuccess} onChange={() => setData({loginsuccess: !data['loginsuccess']})}/>
            <label>Успех авторизации</label>
        </div>
    );
}

export default Login;