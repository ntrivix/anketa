@extends('layouts.app')

@section('content')
<div class="container">
    <div class="row">
        <div class="col-md-8 col-md-offset-2">

            <div class="panel panel-default">
                <div class="panel-heading">Ankete</div>

                <div class="panel-body">
                    <ul class="list-group">
                        @foreach ($aktivne_ankete as $anketa)
                            <a href="anketa/{{$anketa->ID_ANKETE}}">
                                <li class="list-group-item">
                                    <span class="badge">{{$anketa->preostaloVreme()}}</span>
                                    {{$anketa->IME}}
                                </li>
                            </a>
                        @endforeach
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
