import {React, useContext, useEffect, useState} from 'react';
import { Link, useNavigate } from 'react-router-dom';
import AuthContext from '../../context/AuthContext';
import '../../static/css/auth.css'

import localBackgroundImage from '../../assets/images/2.jpeg';

function Register() {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [birthday, setBirthday] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");

  const {registerUser} = useContext(AuthContext);
  
  const navigate = useNavigate();

  if (registerUser.user) {
      navigate('/');
  }
  
  useEffect(() => {
  document.body.style.backgroundImage = `url(${localBackgroundImage})`;
  return () => {
      document.body.style.backgroundImage = '';
  };
  }, []);

  const handleSubmit = async e => {
    e.preventDefault();
    registerUser(email, username, birthday, password, password2);
  };

  return (
    <div className='auth-page'>
      <form className='auth-form' onSubmit={handleSubmit}>
        <div className='form-field'>
          <label>Почта</label>
          <input
              type="email"
              name="email"
              onChange={e => setEmail(e.target.value)}
          />
        </div><br />
        <div className='form-field'>
          <label>Имя пользователя</label>
          <input
              type="text"
              name="username"
              onChange={e => setUsername(e.target.value)}
          />
        </div><br />
        <div className='form-field'>
          <label>День рождения</label>
          <input
              type="date"
              name="birthday"
              onChange={e => setBirthday(e.target.value)}
          />
        </div><br />
        <div className='form-field'>
          <label>Пароль</label><br />
          <input
              type="password"
              name="password"
              onChange={e => setPassword(e.target.value)}
          />
        </div>
        <div className='form-field'>
          <label>Повторите пароль {(password && password === password2) && <span className='password-ok'>Пароли совпадают</span>} </label>
          <input
              type="password"
              name="password2"
              onChange={e => setPassword2(e.target.value)}
          />
        </div><br />
        <button type="submit">Зарегистрироваться</button>
        <Link className='auth-link' to='/login'>Ко входу</Link>
      </form>
    </div>
  );
}

export default Register;