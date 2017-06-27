<?php
/**
 * User: Nikol
 * Date: 27.6.2017.
 * Time: 22.54
 */

namespace App;


use Illuminate\Database\Eloquent\Model;

class Cas extends Model
{
    protected $table = "CAS";
    protected $primaryKey = "ID_CAS";

    public function Predmet(){
        return $this->belongsTo(Predmet::class,"ID_PREDMET","ID_PREDMET");
    }

}