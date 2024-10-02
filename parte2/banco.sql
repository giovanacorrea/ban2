create table pessoa(
	idpessoa int NOT NULL UNIQUE,
	nome varchar(100) NOT NULL,
	telefone varchar(100) NOT NULL, 
	endereco varchar(100) NOT NULL,
	primary key (idpessoa)
);


create table hospede(
	idhospede int NOT NULL UNIQUE,
	idpessoa int NOT NULL,
	primary key (idhospede),
	foreign key (idpessoa) references pessoa 
);


create table acompanhante(
	idacompanhante int NOT NULL UNIQUE,
    idpessoa int NOT NULL,
	idhospede int NOT NULL,
	nome varchar(100) NOT NULL,
	primary key (idacompanhante),
	foreign key (idpessoa) references pessoa,
	foreign key (idhospede) references hospede
);

create table quarto(
	codquarto int NOT NULL UNIQUE, -- será o número do quarto
	tipo_quarto varchar(100) NOT NULL,
	qtdcamas int NOT NULL,
	preco float NOT NULL,
	descricao varchar(100) NOT NULL,
	frigobar varchar(10) NOT NULL,
	banheira varchar(10) NOT NULL,
	primary key (codquarto)
);


create table reserva(
	idreserva int NOT NULL UNIQUE,
	idhospede int NOT NULL,
	codquarto int NOT NULL,
	estado varchar(50) NOT NULL,
	datainicio date NOT NULL,
	dataFim date NOT NULL,
	valorDesconto float,
	primary key (idreserva),
	foreign key (idhospede) references hospede,
	foreign key (codquarto) references quarto
);


create table consumo_frigobar(
	idconsumo int NOT NULL UNIQUE,
	idreserva int NOT NULL,
	item varchar(100) NOT NULL,
	quantidade int,
	data date,
	primary key (idconsumo),
	foreign key (idreserva) references reserva
); 


create table cancelamento(
	idcancelamento int NOT NULL UNIQUE,
	idreserva int NOT NULL,
	dataCancelamento date,
	primary key (idcancelamento),
	foreign key (idreserva) references reserva
); 
