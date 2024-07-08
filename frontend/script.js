
const SEREVER = "http://127.0.0.1:5000"

const check_late = () => axios.get(SEREVER + '/cheak-if-late')
const showMenu = () => document.getElementById("dropdownMenu").style.visibility = 'visible';
const hideMenu = () => document.getElementById("dropdownMenu").style.visibility = 'hidden';
const toggleMenu = () => {
    el = document.getElementById("dropdownMenu");
    style = window.getComputedStyle(el);
    if (style.visibility == 'hidden') {
        showMenu()
        document.getElementById("dropdownMenu").style.animation = 'slideright 0.5s';
    } else {
        document.getElementById("dropdownMenu").style.animation = 'slideleft 0.5s forwards';
        setTimeout(hideMenu, 400)

    }
}
const hideOnResize = () => {
    if (window.innerWidth >= 500) {
        document.getElementById("dropdownMenu").style.visibility = 'hidden';
    }
};
window.onresize = hideOnResize;
document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file');
    const fileLabel = document.getElementById('fileLabel');

    fileInput.addEventListener('change', function (event) {
        const fileName = event.target.files[0] ? event.target.files[0].name : 'Upload image';
        fileLabel.textContent = fileName;
    });
});

const showBooksDashboard = () => {
    document.getElementById("usersNav").style.background = 'none';
    document.getElementById("loansNav").style.background = 'none';
    document.getElementById("booksNav").style.background = '#271956';
    document.getElementById("users").style.visibility = 'hidden';
    document.getElementById("loans").style.visibility = 'hidden';
    document.getElementById("books").style.visibility = 'visible';
}

const showUsersDashboard = () => {
    document.getElementById("booksNav").style.background = 'none';
    document.getElementById("loansNav").style.background = 'none';
    document.getElementById("usersNav").style.background = '#271956';
    document.getElementById("books").style.visibility = 'hidden';
    document.getElementById("loans").style.visibility = 'hidden';
    document.getElementById("users").style.visibility = 'visible';
}

const showLoansDashboard = () => {
    document.getElementById("usersNav").style.background = 'none';
    document.getElementById("booksNav").style.background = 'none';
    document.getElementById("loansNav").style.background = '#271956';
    document.getElementById("books").style.visibility = 'hidden';
    document.getElementById("users").style.visibility = 'hidden';
    document.getElementById("loans").style.visibility = 'visible';
}

const login = (event) => {
    event.preventDefault();
    const user_name = document.getElementById("username").value;
    const user_password = document.getElementById("password").value;

    axios.post(SEREVER + "/login", {
        "user_name": user_name,
        "user_password": user_password
    }, {
        withCredentials: true
    }).then(() => {
        return axios.get(SEREVER + "/check-admin", {
            params: {
                "user_name": user_name
            },
            withCredentials: true
        });
    }).then((res) => {
        if (res.data.user_permission) {
            window.location.href = "admin-dashboard.html";
        } else {
            window.location.href = "books.html";
        }
    })
}

const register = (event) => {
    event.preventDefault();
    user_name = document.getElementById("username_r").value
    user_email = document.getElementById("email_r").value
    user_password = document.getElementById("password_r").value
    user_password_check = document.getElementById("password_r_2").value


    if (user_password != user_password_check) {
        document.getElementById("registerError").innerHTML= '<div style="color: red">password doesn`t match, please renter password</div>'
        return
    }

    axios.post(SEREVER + "/register", {
        "user_name": user_name,
        "user_email": user_email,
        "user_password": user_password
    }, {
        withCredentials: true
    }).then(() => {
        window.location.href = "books.html";
    }).catch(() => {
        document.getElementById("registerError").innerHTML= '<div style="color: red">User name taken</div>'
    })
}

const getAllBooks = () => {
    axios.get(SEREVER + "/available-books")
        .then((res) => {
            books = res.data
            const bookList = books.map(book => `<div class="book-card-container" onclick = "openBookMoadl(${book.book_id})">
                                                    <div><img src = "${SEREVER}/images/${book.image_file_name}" class ="book-image-list"></div>
                                                    <div class="card-main-text"> ${book.title} </div>
                                                    <div> ${book.author} </div>
                                                </div>`).join("");
            document.getElementById("bookList").innerHTML = `${bookList}`;
        })
}

const openBookMoadl = (id) => {
    axios.get(SEREVER + `/book/${id}`)
        .then((res) => {
            book = res.data
            console.log(book)
            document.getElementById("imageCard").innerHTML = `<img src = "${SEREVER}/images/${book.image_file_name}" class="image-card">`
            document.getElementById("bookTitle").innerHTML = `${book.title}`
            document.getElementById("bookAuthor").innerHTML = `${book.author}`
            document.getElementById("bookCategory").innerHTML = `${book.category}`
            document.getElementById("loanType").innerHTML = `Available to loan for ${book.loan_type} days`
            document.getElementById("bookDescription").innerHTML = `/${book.description}`
            document.getElementById("loanBookCardButton").setAttribute("onclick", `loanBook('${id}')`);

            document.getElementById("bookCardModal").style.visibility = 'visible';
        })
}

const loanBook = (id) => {
    axios.post(SEREVER + "/create-loan", {
        'book_id': id
    },
        { withCredentials: true })
        .then(() => { location.reload() })
        .catch((error) => {
            const errorMessage = error.response.data['error'];
            document.getElementById("loanError").innerHTML = `<div style="color: red;">${errorMessage}</div>`;
        })

}

const adminBookList = () => {
    axios.get(SEREVER + "/all-books")
        .then((res) => {
            const books = res.data;

            const loanTypeMapping = {
                5: 'A',
                7: 'B',
                10: 'C'
            };

            const bookList = books.map(book => {
                const loanType = loanTypeMapping[book.loan_type] || book.loan_type;

                return `<tr class = "tr">
                            <td class= "td">${book.title}</td>
                            <td class= "td">${book.author}</td>
                            <td class= "td">${loanType}</td>
                            <td class= "td">${book.is_loaned ? 'Yes' : 'No'}</td>
                            <td class= "td"><button class= "edit-button" onclick="openUpdModal(${book.book_id})">✎</button>
                                            <button class= "edit-button" style="font-weight: bold;" onclick="openDeleteModal(${book.book_id})">🗑</button></td>
                        </tr>`;
            }).join("");

            document.getElementById("bookList").innerHTML += bookList;
        })
        .catch(error => {
            console.error('Error fetching books:', error);
        });
}

const openDeleteModal = (id) => {
    document.getElementById("delete-button-modal").setAttribute("onclick", `deleteBook('${id}')`);
    document.getElementById("delete-modal-container").style.visibility = 'visible';
    document.getElementById("dlt-errorMassege").innerHTML = '';
}

const openUpdModal = (id) => {
    document.getElementById("updForm").setAttribute("onsubmit", `updateBook(event, '${id}')`);
    document.getElementById("update-modal-container").style.visibility = 'visible';
    document.getElementById("upd-errorMassege").innerHTML = '';
}

const closeModal = (modal) => document.getElementById(modal).style.visibility = 'hidden';

const deleteBook = (id) => {
    axios.delete(SEREVER + `/delete-book/${id}`, { withCredentials: true }).then(() => {
        location.reload();
    }).catch((error) => {
        errorMesage = error.response.data['error']
        document.getElementById("dlt-errorMassege").innerHTML = `<div style = color:red >${errorMesage} </div>`
    })
}

const searchBooks = () => {
    const query = document.getElementById("search-input").value.trim();
    if (query) {
        axios.get(SEREVER + `/search-books`, {
            params: {
                title: query
            }
        })
            .then((response) => {
                const books = response.data;
                const bookList = books.map(book =>
                    `<div class="book-card-container">
                    <div><img src="${SEREVER}/images/${book.image_file_name}" class="book-image-list"></div>
                    <div class="card-main-text">${book.title}</div>
                </div>`).join("");
                document.getElementById("bookList").innerHTML = bookList;
            })
            .catch((error) => {
                console.error('Error searching books:', error);
            });
    }
}

const addBook = (event) => {
    event.preventDefault();
    let title = document.getElementById("title").value.trim();
    let author = document.getElementById("author").value.trim();
    let description = document.getElementById("description").value.trim();
    let category = document.getElementById("category").value.trim();
    let fileInput = document.getElementById("file");
    let loanType = document.getElementById("loan_type").value;

    if (title && author && description && category && loanType) {
        let formData = new FormData();
        formData.append("title", title);
        formData.append("author", author);
        formData.append("description", description);
        formData.append("category", category);
        formData.append("loan_type", loanType);

        // Append file if it exists
        if (fileInput.files.length > 0) {
            formData.append("file", fileInput.files[0]);
        }

        axios.post(SEREVER + `/add-book`, formData, {
            withCredentials: true,
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).catch(error => {
            const errorMessage = error.response.data['error'];
            document.getElementById("addBookError").innerHTML = `<div style="color: red;">${errorMessage}</div>`;
        });
    }
}

const updateBook = (event, bookId) => {
    event.preventDefault();

    const updatedBook = {
        title: document.getElementById('upd-title').value,
        author: document.getElementById('upd-author').value,
        description: document.getElementById('upd-description').value,
        category: document.getElementById('upd-category').value,
        loan_type: document.getElementById('upd-loan_type').value,
        // Include image data if an image is selected
        image: document.getElementById('upd-file').files[0] // Assuming you have an input type file with id 'upd-file'
    };

    const formData = new FormData();
    formData.append('title', updatedBook.title);
    formData.append('author', updatedBook.author);
    formData.append('description', updatedBook.description);
    formData.append('category', updatedBook.category);
    formData.append('loan_type', updatedBook.loan_type);
    if (updatedBook.image) {
        formData.append('image', updatedBook.image);
    }
    const config = {
        headers: {
            'Content-Type': updatedBook.image ? 'multipart/form-data' : 'application/json'
        },
        withCredentials: true
    };

    axios.put(SEREVER + `/update-book/${bookId}`, formData, config)
        .then(() => {
            location.reload();
        })
        .catch(error => {
            const errorMessage = error.response.data['error'];
            document.getElementById("upd-errorMassege").innerHTML = `<div style="color: red;">${errorMessage}</div>`;
        });
}

const addUser = (event) => {
    event.preventDefault();
    let userName = document.getElementById("username").value.trim();
    let userEmail = document.getElementById("userEmail").value.trim();
    let tempPassword = document.getElementById("password").value.trim();

    console.log("Attempting to add user:", userName, userEmail); // Log user details

    axios.post(SEREVER + "/add-user", {
        'user_name': userName,
        'user_email': userEmail,
        'user_password': tempPassword
    }, {
        withCredentials: true
    })
        .then(() => {
            location.reload();
        })
        .catch((error) => {
            const errorMessage = error.response.data['error'];
            document.getElementById("addUserError").innerHTML = `<div style="color: red;">${errorMessage}</div>`;
        });
}

const adminUserList = () => {
    axios.get(SEREVER + "/all-users", {
        withCredentials: true
    })
        .then((res) => {
            const users = res.data;
            const pLvlMapping = {
                'A': 'Admin',
                'U': 'User'
            };

            const userList = users.map(user => {
                const lvl = pLvlMapping[user.premission_level] || user.premission_level;

                return `<tr class = "tr">
                        <td class = "td">${user.user_name}</td>
                        <td class = "td">${user.user_email}</td>
                        <td class = "td">${lvl}</td>
                        <td class= "td"><button class= "edit-button" onclick="openUpdModalUser(${user.user_id})">✎</button>
                                            <button class= "edit-button" style="font-weight: bold;" onclick="openUsrDeleteModal(${user.user_id})">🗑</button></td>
                    </tr>`;
            }).join("");

            document.getElementById("userlist").innerHTML += userList;
        }).catch(error => {
            console.error('Error fetching users:', error)
        })
}

const deleteUser = (id) => {
    axios.delete(SEREVER + `/delete-user/${id}`, { withCredentials: true }).then(() => {
        location.reload();
    }).catch((error) => {
        errorMesage = error.response.data['error']
        document.getElementById("dltUsrError").innerHTML = `<div style = color:red >${errorMesage} </div>`
    })
}

const openUpdModalUser = (id) => {
    document.getElementById("updUsrForm").setAttribute("onsubmit", `updateUser(event, '${id}')`);
    document.getElementById("updUserContainer").style.visibility = 'visible';
    document.getElementById("updUsrError").innerHTML = '';
}

const openUsrDeleteModal = (id) => {
    document.getElementById("dltButtonUser").setAttribute("onclick", `deleteUser('${id}')`);
    document.getElementById("delete-user-container").style.visibility = 'visible';
    document.getElementById("dltUsrError").innerHTML = '';
}

const updateUser = (event, id) => {
    event.preventDefault();

    const userName = document.getElementById('updUserName').value.trim();
    const userEmail = document.getElementById('updUserEmail').value.trim();
    const userPassword = document.getElementById('updUserPassword').value.trim();
    const userLevel = document.getElementById('updUserLvl').value;

    const data = {};
    if (userName) data.user_name = userName;
    if (userEmail) data.user_email = userEmail;
    if (userPassword) data.user_password = userPassword;

    axios.put(SEREVER + `/update-user/${id}`, data, {
        withCredentials: true
    })
        .then(response => {
            if (userLevel) {
                if (userLevel === 'A') {
                    return axios.put(SEREVER + `/make-admin/${id}`, {}, {
                        withCredentials: true
                    });
                } else if (userLevel === 'U') {
                    return axios.put(SEREVER + `/remove-admin/${id}`, {}, {
                        withCredentials: true
                    });
                }
            } else {
                return Promise.resolve(response);
            }
        })
        .then(() => {
            location.reload();
        })
        .catch(error => {
            const errorMessage = error.response?.data?.error || 'An error occurred';
            document.getElementById('updUsrError').innerHTML = `<div style="color: red;">${errorMessage}</div>`;
        });
}

const adminLoanList = () => {
    axios.get(SEREVER + "/all-loans", {
        withCredentials: true
    })
        .then((res) => {
            const loans = res.data;
            console.log(res.data);
            const loanList = loans.map(loan => {
                return `<tr class = "tr">
                        <td class= "td">${loan.user_name}</td> 
                        <td class= "td">${loan.book_title}</td>
                        <td class= "td">${loan.loan_date}</td>
                        <td class= "td">${loan.return_date}</td>
                        <td class= "td">${loan.is_late ? 'Yes' : 'No'}</td>
                        <td class= "td"><button onclick="openReturnModal(${loan.loan_id})" class= "edit-button" style="font-weight: bold;">☇</button></td>
                        <td class= "td"><button onclick="openExtendModal(${loan.loan_id})" class= "edit-button">✚</button></td>
                    </tr>`
            }).join("");

            document.getElementById("loanlist").innerHTML += loanList;
        })
}

const openReturnModal = (id) => {
    document.getElementById("returnLoanBtn").setAttribute("onclick", `returnBook('${id}')`);
    document.getElementById("returnLoanContainer").style.visibility = 'visible';
    document.getElementById("extendError").innerHTML = '';
}

const openExtendModal = (id) => {
    document.getElementById("extendLoanBtn").setAttribute("onclick", `extendBook('${id}')`);
    document.getElementById("extendLoanContainer").style.visibility = 'visible';
    document.getElementById("extendError").innerHTML = '';
}

const returnBook = (id) => {
    axios.get(SEREVER + `/return-book/${id}`, { withCredentials: true }).then(() => {
        closeModal('returnLoanContainer')
    }).catch((error) => {
        errorMesage = error.response.data['error']
        document.getElementById("returnError").innerHTML = `<div style = color:red >${errorMesage} </div>`
    })
}

const extendBook = (id) => {
    axios.get(SEREVER + `/extend-loan/${id}`, { withCredentials: true }).then(() => {
        closeModal('extendLoanContainer')
    }).catch((error) => {
        errorMesage = error.response.data['error']
        document.getElementById("extendError").innerHTML = `<div style = color:red >${errorMesage} </div>`
    })
}

const userLateLoans = () => {
    axios.get(SEREVER + `/late-loans`)
        .then((res) => {
            books = res.data
            const bookList = books.map(book => `<div class="book-card-container" onclick = "openBookMoadl(${book.book_id})">
                                                    <div><img src = "${SEREVER}/images/${book.image_file_name}" class ="book-image-list"></div>
                                                    <div class="card-main-text"> ${book.title} </div>
                                                    <div> ${book.author} </div>
                                                </div>`).join("");
            document.getElementById("loanList").innerHTML = `${bookList}`;
        })
}


const getAllLoans = () => {
    axios.get(SEREVER + "/user-loans", { withCredentials: true })
        .then((res) => {
            const books = res.data;
            const bookList = books.map(book => `
                <div class="book-card-container">
                    <div><img src="${SEREVER}/images/${book.image_file_name}" class="book-image-list" alt="${book.title}"></div>
                    <div class="card-main-text">${book.title}</div>
                    <div>${book.author}</div>
                    ${book.is_late ? `<button class="b-default late-return-button" onclick="returnUserBook(${book.loan_id})">Late - Return Book</button>` : `<button class="b-default" onclick="returnUserBook(${book.loan_id})">Return Book</button>`}
                </div>`).join("");
            document.getElementById("loanList").innerHTML = bookList;
        })
        .catch((error) => {
            console.log("Error fetching user loans:", error);
        });
}

const returnUserBook = (loan_id) => {
    axios.get(SEREVER + `/return-book/${loan_id}`, { withCredentials: true })
        .then((res) => {
            console.log(res.data.message);
            getAllLoans();
        })
        .catch((error) => {
            console.log("Error returning book:", error);

        });
};

const checkAdminStatus = (id) => {
    axios.get(SEREVER + "/check-admin", { withCredentials: true })
        .then((res) => {
            if (res.data.user_permission) {
                document.getElementById(id).style.display = "block";
            }
        })
        .catch((error) => {
            console.log("Error checking admin status:", error);
        });
};

const goToRegularWebsite = () => {
    window.location.href = "books.html";
};

const goToDashboard = () => {
    window.location.href = "admin-dashboard.html";
};