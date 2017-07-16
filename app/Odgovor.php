<?php
/**
 * User: Nikol
 * Date: 15.7.2017.
 * Time: 13.03
 */

namespace App;


use Illuminate\Database\Eloquent\Model;

class Odgovor extends Model
{
    protected $table = "ODGOVOR";
    protected $primaryKey = "ID_ODGOVOR";
    public $timestamps = false;
}