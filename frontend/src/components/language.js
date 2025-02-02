import React, { Component } from 'react';

class LanguageSelector extends Component {
    constructor(props) {
        super(props);
        this.setLang = this.setLang.bind(this);
    }

    setLang(event) {
        this.props.setLang(event.target.value);
    }

    render() {
        return (
            <div>
                <label className="block mb-2" htmlFor="lang">
                    Language
                </label>
                <select
                    id="lang"
                    onChange={this.setLang} // Use the prop function here
                    className="w-full p-2 border border-gray-300 rounded mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                    <option value="en">English</option>
                    <option value="hi">Hindi</option>
                    <option value="kn">Kannada</option>
                    <option value="ta">Tamil</option>
                    <option value="te">Telugu</option>
                    <option value="bn">Bengali</option>
                    <option value="ml">Malayalam</option>
                    <option value="gu">Gujarati</option>
                    <option value="mr">Marathi</option>
                    <option value="pa">Punjabi</option>
                </select>
            </div>
        );
    }
}

export default LanguageSelector;
