const express = require('express');
const router = express.Router();

const UserController = require('../controllers/UserController.js');
const FunctionController= require('../controllers/FunctionController');

// Middleware para proteger rutas (solo usuarios autenticados)
const isAuthenticated = (req, res, next) => {
    if (req.session && req.session.id_usuario) {
        next(); // Continúa si la sesión existe
    } else {
        res.redirect('/login'); // Redirige al login si no hay sesión
    }
};

router.get('/list', FunctionController.list);

//
router.post('/crear_usuario', UserController.createUser);

// Ruta protegida: dashboard
router.get('/dashboard', isAuthenticated, FunctionController.dashboard); // Solo accesible si está autenticado

// Ruta protegida: modificar_datos
router.get('/modificar_datos', isAuthenticated, FunctionController.modificar_datos);

// Ruta protegida: modificar_datos
router.post('/cambio_datos', isAuthenticated, FunctionController.cambio_datos); // Solo accesible si está autenticado

// Ruta protegida: modificar_datos
router.post('/cambio_datos_ca/:id_cuerpo_a', isAuthenticated, FunctionController.cambio_datos_ca); // Solo accesible si está autenticado

// Ruta protegida: modificar_cuerpo_a
router.get('/mod_reg/:id_cuerpo_a', isAuthenticated, FunctionController.cambioReg); // Solo accesible si está autenticado

// Ruta protegida: modificar_cuerpo_a
router.get('/del_reg/:id_cuerpo_a', isAuthenticated, FunctionController.delReg); // Solo accesible si está autenticado

//ruta protegida ver registro
router.get('/ver_registro/:id_cuerpo_a', isAuthenticated, FunctionController.verRegistro);

//ruta protegida de datos personales
router.get('/datos_personales',isAuthenticated, FunctionController.datosPersonales);

//Crear nuevo usuario
router.post('/user_reg', UserController.save);

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

// Ruta para cerrar sesión
router.get('/logout', (req, res) => {
    req.session.destroy(() => {
        res.redirect('/login'); // Redirige al login después de cerrar sesión
    });
});

module.exports=router;