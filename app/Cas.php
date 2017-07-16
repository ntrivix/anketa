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
    protected $with=["Predmet"];
    public function Predmet(){
        return $this->belongsTo(Predmet::class,"ID_PREDMET","ID_PREDMET");
    }

    public function predavac(){
        return $this->hasOne(Predavac::class, 'ID_PREDAVAC', 'ID_PREDAVAC');
    }

}