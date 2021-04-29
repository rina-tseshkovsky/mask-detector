<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')
		
        <!-- 
        zadnitsa indeitsa 
        -->

        <h2>Restoreing Database</h2>
        <form action="/rst-db" method="post">
            File Name: <input name="file_name" type="text" /><br>
            <input value="Restore This File" type="submit" />
            <input type="submit" name="bt1" value="Back" />
        </form>  

	</body>    
</html>