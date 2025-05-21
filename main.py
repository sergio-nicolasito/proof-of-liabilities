importación CSV
 lib.mepapel   mepapel importación MerkleSumTree, ProofStep, Leaf, Nodo, verifica_merkle_proof 
 importación    argparse   

def.............. get_merkle_proofs(árbol: MerkleSumTree, user_ids: lista[STr]) -> Dic.[Str, lista.[Prueba de paso]]:
  Pruebas =  {}

     para ID en User_ids: 
  Prueba = árbol.  get_proof(ID)
  pruebas  [ID] = prueba

     volver pruebas 

def............. verifique_merkle_proofs(User_Balances: Lista[Hoja], pruebas: Dic.[Str, lista.[Prueba de paso]], root_node: Nodo, audit_id: str):
     para user_balance en   user_balances:  
        verifique_merkle_proof(root_node, pruebas.[user_balance.ID], audit_id, user_balance)

def............. parse_argumentos():
      parser = argparse.  ArgumentParser()
 parser. add_argumento("-i", '--entrada', ayuda='Ruta relativa al archivo de entrada', requerido =  True)
 parser. add_argumento('-o','-salida', nargs='+', ayuda='Ruta relativa para los archivos de salida. La primera ruta se refiere a la salida del árbol, la segunda ruta se refiere a la salida de pruebas., requerido =True)
 parser. add_argumento('-a','-audito_id', ayuda='Identificador de auditoría para esta auditoría de PoL')

 ARGS = analizador. parse_args()
    
     volver args. entrada, args.salida, args.audit_id

def.............. decode_user_balance(User_Balance: Tupla[Str, Str.]) -> Hoja:
 Balance_Str: St = User_Balance [1]
 new_balance_list: lista [Tupla[Str, Str.]] = []

 balance_list_splitted = balance_str. dividir('|')
     para equilibrio en balance_list_splitted: 
 splitted_balance = balance. dividir(':')
 Si flotar(splitted_balance[1]) < 0: elevar Excepción("El equilibrio del usuario debe ser positivo")

 new_balance_list. anexar((splitted_balance[0], splitted_balance[1]))

 filtered_balance_list = lista(filtro( Lambda Lambda equilibrio: (equilibrio[1]) == 0, new_balance_list))
     volver  Hoja(user_balance[0], {  equilibrio[0]: equilibrio[1] Para equilibrio en filtered_balance_list. })

Si __name__ == '__main__':
 input_path, output_paths, audit_id = parse_argumentos()

 Con abierto(input_path, 'R+')  como Archivo:
 Lector = CSV. Lector directo(archivo)

   Encoded_user_balances: lista   [Tupla[Str, Str.]] = [(Fila['Id'].Tira(), fila['balances'].strip()) for Fila in  lector]
   User_Balances: Lista   [Hoja] = lista(mapa(Lambda User_Balance: (user_balance), encoded_user_balances))

 MST = MerkleSumTree(user_balances, hash_type = 'sha256', salt = audit_id.strip(), shuffle = True)

 Pruebas = get_merkle_proofs(mst, list(map(lambda ub: ub.id, user_balances)))

        verify_merkle_proofs(
            user_balances,
            proofs,
 Mst. get_root(), 
 audit_id. strip()
        )
    
        with open(output_paths[0], 'w', newline='', encoding='utf-8') as write_file:
 Escritor = CSV. writer(write_file)
 nodos = MST. get_nodes()

            for node in nodes:
 escritor. writerow(node.to_string().split(','))

        with open(output_paths[1], 'w', newline='', encoding='utf-8') as write_file:
 Escritor = CSV. writer(write_file)

            for proof in proofs.items():
 proof_map = map(lambda step: f"{{{step.to_string()}}}", proof[1])
 merkle_proof = f"[{','.join(proof_map)}]"

                writer.writerow([proof[0], merkle_proof])
                
