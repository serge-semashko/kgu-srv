<?php

class JSON
{
    public static function safeEncode($var)
    {
        function json_fix_cyr($var)
        {
            if (is_array($var))
            {
                $new = array();
 
                foreach ($var as $k => $v)
                   $new[json_fix_cyr($k)] = json_fix_cyr($v);

                $var = $new;
            }
            elseif (is_object($var))
            {
                $vars = get_object_vars($var);
                
                foreach ($vars as $m => $v)
                   $var->$m = json_fix_cyr($v);
            }
            elseif (is_string($var))
            {
                $var = iconv('cp1251', 'utf-8', $var);
            }
            return $var;
        }

        return json_encode(json_fix_cyr($var));
    }
    
    public static function enclose($name, $json)
    {
        return $name . "(" . $json . ");";
    }
}


?>
