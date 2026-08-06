#exercice

1. créer une api avec fastAPI
    Dans l'api ajouter

    - model (sqlAlchemy)
        task (pr la db)
            id int(auto-incrémenté)
            name str
            attribution_email str
            status ( status in [in_progress, done])
            end_date

    - un controller task_controller
        plusieurs points d'entrée :
        - add_task  (route : post, /task)
            * entrée : name, attribution_mail (mail de la pers à qui la ête est attribuée), duration (nbre de jours)
            * nouvelle tache créée ? Elle a son status
                    status = in_progress
            (status in [progress, done])
            * quand on ajoute une tâche, un email devra être envoyé
            à la personne qui doit effectuer la tâche
            * sauvegarde de la tâche en DB (avec sqlAlchemy)
            /!\ date de fin dans l'objet en db, duration dans le dto
        - get_task  (route : get, /task)
            * entrée (email, limit, status, page) : 
                + si un email a été spécifié on récup les tâches de l'email
                + si un limit : on récupère le nombre "limit" de records ; si pas de limit, on limit à 10 ; et limit est maxé à de 100.
                + si un status est spécifié, on ne récup que le status correspondant
                + page : un int qui permet de récup la page ; par def, c'est la page 1.
        - change_task_status : (put, /task/{id})
            #    (pour récup id dans le code :
            #    id:int = Path(), Attention c'est le Path de FastAPI et pas celui qui va lire la structure fichier)
            * entrée: status
            modifier le status de la tâche avec l'id spécifié
            on ne peut changer l'état de la tâche que si on n'est pas arrivé à la date d'échéance.
        - delete_task : (delete, /task/{id})
            * supprimer la tâche 'id'
            * on ne peut pas supprimer une tâche "done"
            * envoi d'un mail à la personne qui doit effectuer la tâche pour signaler que la tâche n'existe plus.
