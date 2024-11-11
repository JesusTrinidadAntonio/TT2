const express = require('express');
const router = express.Router();

const UserController = require('../controllers/UserController.js');
const FunctionController= require('../controllers/FunctionController');

router.get('/list', FunctionController.list);

//Redireccionamos a sugerencias
router.get('/sugerencias', FunctionController.sug);

//Redireccionamos a registros
router.get('/registros',FunctionController.reg);

//Funcion read mysql
router.get('/', FunctionController.home);

//Funcion add mysql
router.post('/add',FunctionController.save);

//funcion delete mysql
router.get('/delete/:id_usuario',FunctionController.delete);

//Redireccion a la pantalla de modificar
router.get('/update/:id_usuario',FunctionController.edit);

//Funcion update mysql
router.post('/update/:id_usuario',FunctionController.update);

//Redireccion con el boton de iniciar sesion
router.get('/login', UserController.login);

//Redireccion con el boton de registrate
router.get('/signin', UserController.signin);

//Agregar sugerencias
router.post('/sugg', FunctionController.sugg);

module.exports=router;