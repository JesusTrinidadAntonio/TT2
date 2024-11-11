const express = require('express');
const path= require('path');//Modulo que une directorios
const morgan= require('morgan');
const mysql= require('mysql');
const myConnection= require('express-myconnection');

const app = express();

//importando rutas 
const usuarioRoutes= require('./routes/glbRoutes');

//Montar la pagina en un servidor, se le asigna un puerto
app.set('port', process.env.PORT || 3000);

//Configuramos el motor de plantillas
app.set('view engine', 'ejs');

/*_dirname es una constante de nodejs que se encarga de dar 
la ruta del archivo que lo ejecuta*/
app.set('views', path.join(__dirname, 'views'));

//Configuramos los middlewares
app.use(morgan('dev'));//Registra las peticiones entrantes


//Configuracion de mysql
app.use(myConnection(mysql, {
    host: 'localhost',
    user: 'sergio',
    password: 'password',
    port:3306,
    database: '2024_b049'
},'single'));

//Nos sirve a que podamos entender los datos del formulario
app.use(express.urlencoded({
    extended: false
}));
//Configuramos la rutas o peticiones
app.use('/', usuarioRoutes);

//archivos estaticos
app.use(express.static(path.join(__dirname, 'public')));

//Iniciando en servidor de manera local
app.listen(app.get('port'), ()=>{
    console.log('Servidor en el puerto 3000');
});