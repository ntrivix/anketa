<?php

namespace App;

use Carbon\Carbon;
use Illuminate\Notifications\Notifiable;
use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable
{
    use Notifiable;
    protected $table = "STUDENT";

    protected $primaryKey = "ID_STUDENT";

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'IME', 'PREZIME', 'email', 'INDEKS', 'JMBG', 'password', 'NADIMAK'
    ];

    /**
     * The attributes that should be hidden for arrays.
     *
     * @var array
     */
    protected $hidden = [
        'password', 'remember_token',
    ];

    public function casovi(){
        return $this->belongsToMany(Cas::class, "STUDENT_NA_CASU", "ID_STUDENT", "ID_CAS");
    }

    public function grupa(){
        return $this->belongsToMany(Grupa::class, "STUDENT_U_GRUPI", "ID_STUDENT", "ID_GRUPA");
    }

    public function aktivnaGrupa(){
        return $this->grupa()->where([["AKTIVNA_OD","<", Carbon::now()],["AKTIVNA_DO",">", Carbon::now()]])->get()->first();
    }

    public function sviCasovi(){
        $c1 = $this->casovi;
        $c2 = $this->grupa()->where([["AKTIVNA_OD","<", Carbon::now()],["AKTIVNA_DO",">", Carbon::now()]])->get()->first()->casovi;

        $included = [];
        $all = [];
        foreach ($c2 as $c){

            $all[] = $c;
            $included[$c->ID_CAS] = true;
        }
        foreach ($c1 as $c){
            if (!isset($included[$c->ID_CAS]))
            {

                $all[] = $c;
                $included[$c->ID_CAS] = true;
            }
        }
        usort($all, function($a, $b)
        {
            if ($a->ID_PREDMET == $b->ID_PREDMET)
            {
                if ($a->TIP_CASA == 'P')
                    return -1;
                return 0;
            }
            return strcmp($a->ID_PREDMET, $b->ID_PREDMET);
        });
        return $all;
    }
}
