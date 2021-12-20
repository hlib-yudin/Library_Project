const defaultNavbar = `
<li class="nav-item"> <a class="nav-link " href="{{url_for('catalogue')}}">Каталог</a> </li>
<li class="nav-item"> <a class="nav-link " aria-current="page" href="{{url_for('basket')}}">Кошик</a> </li>
<li class="nav-item" id = 'orders'> <a class="nav-link " aria-current="page" href="{{url_for('page_for_orders')}}">Замовлення</a> </li>`;

const librarianNavbar = {
    'add books' : `<li class="nav-item"> <a class="nav-link" aria-current="page" href="{{url_for('addBook')}}">Додати книгу</a> </li>`,
    'delete books': `<li class="nav-item" id = 'delete books'> <a class="nav-link " href="{{url_for('removeBook')}}">Видалити Книгу</a> </li>`,
    'issue/accept books' : `<li class="nav-item" id = 'issue/accept books'> <a class="nav-link " aria-current="page" href="{{url_for('issuebooks')}}">Видати книгу</a> </li>`,
    'analytics': `<li class="nav-item"> <a class="nav-link" aria-current="page" href="{{url_for('analytics')}}">Аналітика</a> </li>`,
};

const loginIcon = `
    <a class="uk-navbar-item uk-link-muted tm-navbar-button uk-icon"
                                    href="{{url_for('signup')}}" uk-icon="icon: user; ratio:2" id="account">
        <svg width="40" height="40" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
            <circle fill="none" stroke="white" stroke-width="1.1" cx="9.9" cy="6.4" r="4.4"></circle>
            <path fill="none" stroke="#fff" stroke-width="1.1"
                  d="M1.5,19 C2.3,14.5 5.8,11.2 10,11.2 C14.2,11.2 17.7,14.6 18.5,19.2"></path>
        </svg>
    </a>
`;

const adminNavbar = {
    'register librarians': `<li class="nav-item"> <a class="nav-link" aria-current="page" href="{{url_for('page_for_registering_librarians')}}">Реєстрація бібліотекарів</a> </li>`,
    'analytics': `<li class="nav-item"> <a class="nav-link" aria-current="page" href="{{url_for('analytics')}}">Аналітика</a> </li>`,
};

const setNavbar = (type, permissions) => {
    const navbarNode = document.getElementById('navbarSupportedContent');
    if(type === 'reader'){
        navbarNode.children[0].insertAdjacentHTML('afterbegin', defaultNavbar);
    } else if (type === 'librarian'){
        permissions.forEach(permission => {
            navbarNode.children[0].insertAdjacentHTML('afterbegin',librarianNavbar[permission]);
        });
        navbarNode.children[0].insertAdjacentHTML('afterbegin',`<li class="nav-item"> <a class="nav-link " aria-current="page" href="{{url_for('page_for_returning_books')}}">Повернути книгу</a> </li>`);
    }else if (type === 'unlogged'){
        navbarNode.children[0].insertAdjacentHTML('afterbegin',`<li class="nav-item"> <a class="nav-link " href="{{url_for('catalogue')}}">Каталог</a> </li>`);
    } 
     else {
        permissions.forEach(permission => {
            navbarNode.children[0].insertAdjacentHTML('afterbegin',adminNavbar[permission]);
        });
    }
};
//aria-current="page"
const createNavbar = () => {
    let role = sessionStorage.getItem('status');
    let permissions = sessionStorage.getItem('permissions');
    let login = sessionStorage.getItem('logged');

    if(!permissions){
        permissions = [];
    }

    if(!role){
        role ='unlogged';
    }

    if (typeof permissions === 'string'){
        setNavbar(role,permissions.split(','));
    } else{
        setNavbar(role,permissions);
    }

    addLoggedIcon(login);
};

const addLoggedIcon = (login) => {
    const loginNode = document.getElementById('login_icon');
    if (login === 'undefined') {
        loginNode.insertAdjacentHTML('beforeend', loginIcon);

        return;
    }

    loginNode.insertAdjacentHTML('afterbegin', `<p class="text-white bg-dark">Вітаю, ${login}</p> <a href="{{url_for('signup')}}" class="btn btn-dark btn-lg active" role="button" aria-pressed="true">Вийти</a>`);
};
