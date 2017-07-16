<?php
/**
 * User: Nikol
 * Date: 2.7.2017.
 * Time: 12.58
 */

namespace App;


use Illuminate\Database\Eloquent\Model;

class Anketa extends Model
{
    protected $table = "ANKETA";
    protected $primaryKey = "ID_ANKETE";

    protected $with = ["pitanja", "popunili"];

    public function pitanja(){
        return $this->belongsToMany(Pitanje::class, "PITANJA_ZA_ANKETU", "ID_ANKETE", "ID_PITANJA");
    }

    public function popunili(){
        return $this->belongsToMany(User::class, "POPUNIO_ANKETU", "ID_ANKETE", "ID_STUDENT");
    }

    public function preostaloVreme(){

        $datestr=$this->OTVORENA_DO;//Your date
        $date=strtotime($datestr);//Converted to a PHP date (a second count)

        $diff=$date-time();//time returns current time in seconds
        $days=floor($diff/(60*60*24));//seconds/minute*minutes/hour*hours/day)
        $hours=round(($diff-$days*60*60*24)/(60*60));
        if ($days > 0) {
            if ($days == 1)
                return "otvorena jos 1 dan";
            return "otvorena jos $days dana";
        }
        echo "otvorena jos $hours h";
    }
}