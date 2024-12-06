const express = require('express');
const router = express.Router();

const UserController = require('../controllers/UserController.js');
const FunctionController = require('../controllers/FunctionController');


/**
 * Página de login funcionalidad
 */

        router.get('/', UserController.login);

        //Crear usuario
        router.post('/crear_usuario', UserController.createUser);

        //Crear nuevo usuario
        router.post('/user_reg', UserController.save);

/** 
*
        *Fin de Fucionalidad de LogIn
*
*/



        // Middleware para proteger rutas (solo usuarios autenticados)
        const isAuthenticated = (req, res, next) => {
            if (req.session && req.session.id_usuario) {
                next(); // Continúa si la sesión existe
            } else {
                res.redirect('/'); // Redirige al login si no hay sesión
            }
        };



//Pantalla de home para los usuarios
    router.get('/home',isAuthenticated, FunctionController.home);

/**
 *Dashboard Se requiere estar autenticado e iniciar sesión
*/

        //Mis registros
        router.get('/dashboard', isAuthenticated, FunctionController.dashboard);

        // Datos personales
        router.get('/datos_personales', isAuthenticated, FunctionController.datosPersonales);

        //Realizar medición
        router.get('/instrucciones', isAuthenticated, FunctionController.instrucciones);

        router.get('/resultados', isAuthenticated, FunctionController.resultados);

        //Registros públicos
        router.get('/registros_pub', isAuthenticated, FunctionController.registros_pub);

        //¿Quienes somos?
        router.get('/quienes_somos', isAuthenticated, FunctionController.somos);

        // Cerrar sesión
        router.get('/logout', (req, res) => {
            req.session.destroy(() => {
                res.redirect('/'); // Redirige al login después de cerrar sesión
            });
        });

/**
 * 
 * FIN DASHBOARD
 *  
 * */

/*
        INICIO FUNCIONALIDAD DE USUARIOS REGISTRADOS   

*/

//DATOS DEL USUARIO
        // PANTALLA DE MODIFICACION DE DATOS 
        router.get('/modificar_datos', isAuthenticated, FunctionController.modificar_datos);

        // CAMBIO DE DATOS EN LA BASE DE DATOS
        router.post('/cambio_datos', isAuthenticated, FunctionController.cambio_datos); 


//Datos del cuerpo de agua
    /**Evitamos que se vea el id en el url */
        router.get('/ver_registro/:id_cuerpo_a', isAuthenticated, (req, res) => {
            // Guarda el id_cuerpo_a en la sesión
            req.session.id_cuerpo_a = req.params.id_cuerpo_a;

            // Redirige a la ruta que carga el registro
            res.redirect('/ver_registro');
        });

        //ruta protegida ver registro
        router.get('/ver_registro', isAuthenticated, FunctionController.verRegistro);

        //Redireccionamos para que no se vea el id del cuerpo de agua
            router.get('/mod_reg/:id_cuerpo_a', isAuthenticated, (req, res) => {
            // Guarda el id_cuerpo_a en la sesión
            req.session.id_cuerpo_a = req.params.id_cuerpo_a;

            // Redirige a la ruta que carga el registro
            res.redirect('/mod_reg');
        });


        //Visualizacion de la pantalla de modificar registro (inputs) desde el boton modificar
        router.get('/mod_reg', isAuthenticated, FunctionController.cambioReg); 

        // Boton para eliminar el cuerpo de agua
        router.get('/del_reg/:id_cuerpo_a', isAuthenticated, FunctionController.delReg); 

        // Cambio de los datos del cuerpo de agua en la base de datos (direccion y cuerpo_a)
        router.post('/cambio_datos_ca/:id_cuerpo_a', isAuthenticated, FunctionController.cambio_datos_ca); 



/**Usuario tipo_adm */

router.get('/adminHome', isAuthenticated, FunctionController.admHome);

router.get('/adm_pendientes',isAuthenticated, FunctionController.admPend);

router.get('/aceptar_pub/:id_cuerpo_a',isAuthenticated, FunctionController.aceptarPub);

router.get('/rechazar_pub/:id_cuerpo_a',isAuthenticated, FunctionController.rechazarPub);

router.get('/adm_bugs',isAuthenticated,FunctionController.admBugs);

router.get('/adm_usuarios',isAuthenticated,FunctionController.admUsuarios);

router.get('/pub_reg/:id_cuerpo_a',isAuthenticated, FunctionController.pub_reg);


router.get('/update/:id_usuario', isAuthenticated, FunctionController.edit);


router.get('/list', FunctionController.list);


//Redireccionamos a sugerencias
router.get('/sugerencias', FunctionController.sug);

//Redireccionamos a registros
router.get('/registros', FunctionController.reg);


//Funcion add mysql
router.post('/add', FunctionController.save);


//funcion delete mysql
router.get('/delete/:id_usuario', FunctionController.delete);


//Funcion update mysql
router.post('/update/:id_usuario', FunctionController.update);

//Agregar sugerencias
router.post('/sugg', FunctionController.sugg);

/*
    **Paginas Pendientes o sin usar
*/

//Redireccion con el boton de registrate
router.get('/signin', UserController.signin);

module.exports = router;