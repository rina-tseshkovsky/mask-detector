<html>
    % include('head.tpl')
    <body>
        % include('header.tpl')

        <p> the operation {{op_name}} was succesfully done,<br> press "Back" to return back to the main menu</p>
        <form action="/user-added" method="post">
            <input type="submit" name="bt1" value="Back" />
        </form> 
    </body>    
</html>