const controller={};

//Iniciamos la configuración de la conexion a la base de datos
controller.list= (req,res) => {
    req.getConnection((err, conn) => {
        conn.query('select * from usuario', (err, usuarios) => {
            if(err){
                //En caso de desarrollo utilizar res.json
                //En casos mas profesionales utilizar next(err)
                res.json(err);
            }
            res.render('usuarios_adm',{
                data: usuarios
            });
        });
    });
};

//Guardar datos en la base de datos
controller.save=(req,res)=>{
    const data= req.body;
    req.getConnection((err,conn)=>{
        conn.query('INSERT INTO usuario set ?', [data], (err,usuario)=>{
            console.log(usuario);
            res.redirect('/login');
            console.log(data);
        });
    });
    
};

//Eliminar datos en la base de datos
controller.delete=(req,res)=>{   
    const { id_usuario }=req.params;
    req.getConnection((err,conn)=>{
        conn.query('DELETE FROM usuario where id_usuario = ? ',[id_usuario],(err,rows)=>{
            res.redirect('/');
            
        });
    });
};

controller.edit=(req,res)=>{
    const { id_usuario }=req.params;
    req.getConnection((err,conn)=>{
        conn.query('SELECT * FROM usuario where id_usuario=?',[id_usuario],(err,usuario)=>{
            res.render('usuarios_adm_mod',{
                data: usuario[0]
            });
        });
    });
};

controller.update=(req,res)=>{
    const { id_usuario }=req.params;
    const nuevoUsuario= req.body;
    req.getConnection((err,conn)=>{
        conn.query('UPDATE usuario set ? where id_usuario = ?' , [nuevoUsuario,id_usuario], (err,rows)=>{
            res.redirect('/');
        });
    });
};


controller.home=(req,res)=>{
    res.render('home');
};

controller.sug=(req,res)=>{
    res.render('sugerencias');
};

controller.reg=(req,res)=>{
    req.getConnection((err, conn) => {
        conn.query('select * from cuerpo_agua', (err, registros) => {
            if(err){
                //En caso de desarrollo utilizar res.json
                //En casos mas profesionales utilizar next(err)
                res.json(err);
            }
            res.render('registros',{
                data: registros
            });
        });
    });
};

controller.sugg=(req,res)=>{
    const data= req.body;
    req.getConnection((err,conn)=>{
        conn.query('INSERT INTO sugerencias set ?', [data], (err,sugerencias)=>{
            console.log(sugerencias);
            res.redirect('/');
            console.log(data);
        });
    });
    
};

module.exports=controller;