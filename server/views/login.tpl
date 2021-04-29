
<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')

		<h2>WELCOME!</h2>

        <form action="/login" method="post">
            User Name: <input name="name" type="text" /><br>
            Password: <input name="password" type="text" /><br>
            <input value="Login" type="submit" />
            <input type="submit" name="bt1" value="cancel" />

        </form>  
	</body>    
</html>