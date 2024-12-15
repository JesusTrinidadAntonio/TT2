const controller={};

controller.login = (req, res) => {
    res.render('login', { error: null }); // Renderiza la vista de login
};

controller.signin=(req,res)=>{
    res.render('signin');
};

// Procesar inicio de sesión
controller.createUser = (req, res) => {
    const { correo_usuario, contraseña_usuario } = req.body;

    req.getConnection((err, conn) => {
        if (err) {
            console.error("Error al conectar a la base de datos:", err);
            return res.status(500).send("Error interno del servidor");
        }

        // Verificar credenciales
        conn.query(
            'SELECT id_usuario, tipo_usuario FROM usuario WHERE correo_usuario = ? AND contraseña_usuario = ?',
            [correo_usuario, contraseña_usuario],
            (err, results) => {
                if (err) {
                    console.error("Error al realizar la consulta:", err);
                    return res.status(500).send("Error interno del servidor");
                }

                if (results.length > 0) {
                    // Credenciales válidas, guardar información en sesión
                    const usuario = results[0];
                    req.session.id_usuario = usuario.id_usuario;
                    req.session.tipo_usuario = usuario.tipo_usuario;
                    console.log("Usuario autenticado con ID:", usuario.id_usuario);
                    console.log("Tipo de usuario:", usuario.tipo_usuario);

                    // Redirigir según el tipo de usuario
                    if (usuario.tipo_usuario === 1) {
                        res.redirect('/home');
                    } else if (usuario.tipo_usuario === 2) {
                        res.redirect('/adminhome');
                    } else {
                        res.status(400).send("Tipo de usuario no reconocido");
                    }
                } else {
                    // Credenciales inválidas
                    console.log("Credenciales inválidas para:", correo_usuario);
                    res.render('login', { error: "Correo o contraseña incorrectos" }); // Muestra error
                }
            }
        );
    });
};


//Registro en base de datos de un nuevo usuario
controller.save=(req,res)=>{
    const data= req.body;
    req.getConnection((err,conn)=>{
        conn.query('INSERT INTO usuario set ?', [data], (err,usuario)=>{
            console.log(usuario);
            res.redirect('/');
            console.log(data);
        });
    });
    
};



module.exports=controller;