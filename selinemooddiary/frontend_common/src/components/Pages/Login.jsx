import React, { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthContext from '../../context/AuthContext'
import '../../static/css/auth.css'

function Login() {
    
    const {loginUser} = useContext(AuthContext);

    const navigate = useNavigate();

    if (loginUser.user) {
        navigate('/');
    }
    
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errors, setErrors] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrors([]);
        setLoading(true);

        if (password && email) {
            loginUser(email, password);
        } else {
            if (!email) {
                setErrors([...errors, 'Почта не введена']);
            }
            if (!password) {
                setErrors([...errors, 'Пароль не введён']);
            }
        }

        setLoading(false);

        if (loginUser.user) {
            navigate('/');
        }
    };

    return (
        <div className='auth-page'>
            <form className='auth-form' onSubmit={handleSubmit}>
                <div className='form-field'>
                    <label>Почта</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div><br/>
                <div className='form-field'>
                    <label>Пароль</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div><br/>
                <button type="submit" disabled={loading}>
                    {loading ? 'Загрузка...' : 'Войти'}
                </button>
                {errors.map((error) => {<p className='error-alert' >{error}</p>})}<br/>
                <Link className='auth-link' to='/register'>Зарегистрироваться</Link>
            </form>
        </div>
    );
}

export default Login;